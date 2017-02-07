from collections import defaultdict
from joblib import Parallel, delayed

from kproblog import Term, KProbLog, symbols
from kproblog.core import term_to_string
from kproblog.experiments.common import feature_extraction, model_selection, split_in_blocks, VLABEL, ELABEL
from kproblog.experiments.common import model_selection, extract_subset_parallel, SparseFeatures
from kproblog.experiments.qc_io import one_pkl2dataset, Word2WL_Type
from kproblog.semirings import VoidMonoid, PolynomialSemiring, SetMonoid, PolynomialSemiring, MultisetMonoidOfMonoids, Meta, ShortestPathSemiring
from kproblog.semirings.utils import dict2symbol, sv_add, Obj2Id, nhash_m19, nhash_m13
from kproblog.utils import TimeContext

from sklearn.metrics import accuracy_score
import functools, itertools, glob
import numpy as np
import scipy.sparse as sp
import signal

N_JOBS = 1

word2wl_type = Word2WL_Type()

token_labels, dep_rel = symbols('token_labels, dep_rel')
bow_features, feature_blocks, final_features = symbols('bow_features, feature_blocks, final_features')

dep_rel_edge, spath = symbols('dep_rel_edge, spath')
v2labels, = symbols('v2labels')
config, = symbols('config')

# VARIABLES
V, U, W = symbols('V, U, W')

# CONSTANTS
word, pos, lemma = symbols('word, pos, lemma')
meta, = symbols('meta')

kproblog = KProbLog()

kproblog.declare_destructive_many({
    PolynomialSemiring(): [
        final_features/0,
        dep_rel/2
    ],
    MultisetMonoidOfMonoids(PolynomialSemiring()):[
        token_labels/1,
        bow_features/0,
        feature_blocks/0,
    ],
    MultisetMonoidOfMonoids(MultisetMonoidOfMonoids(PolynomialSemiring())):[
        v2labels/0
    ],
    Meta(): [
        meta/0
    ],
    SetMonoid():[
        config/0
    ]
})

kproblog.declare_additive_many({
    ShortestPathSemiring(): [
        spath/2,
        dep_rel_edge/2,
    ]
})

# VERTEX TO LABELS
@kproblog
def vertex_to_labels_proc(label_dict:token_labels(V), info:meta) -> v2labels:
    v, = info['label_dict'].args
    return {v:label_dict}

# BOW FEATURES
@kproblog
def bow_feat_block_proc(label_dict:token_labels(V), config_set:config) -> bow_features:
    block2feats = {}
    for (feat_type, params), in config_set:
        if feat_type != 'bow': continue
        bow_label_type, = params
        block2feats['bow', bow_label_type] = label_dict[bow_label_type]
    return block2feats

# SHORTEST PATHS ON DEPENDENCY RELATIONS
@kproblog
def cast_to_shortest_path(edge_value:dep_rel(V, W), info:meta) -> dep_rel_edge(V, W):
    v, w = info['edge_value'].args
    edge_label = dict2symbol(edge_value)
    return ShortestPathSemiring.create_from_edge_value(v, w, edge_label=edge_label) # XXX EDGE LABEL HERE

@kproblog
def sp_proc0(edge_value:dep_rel_edge(V, W), info:meta) -> spath(V, W):
    return edge_value

@kproblog
def sp_proc1(edge_value:dep_rel_edge(V, U), sp_value:spath(U, W), _:V != W) -> spath(V, W):
    return edge_value * sp_value

# FEATURE BLOCKS 
@kproblog # BAG OF WORD BLOCKS
def bow_feature_block_proc(feat_block:bow_features) -> feature_blocks:
    return feat_block

@kproblog # SHORTEST PATH BLOCKS
def sp_features_block_proc(spath_value:spath(V, W), v2labels_dict:v2labels, config_set:config) -> feature_blocks:
    block2phi = defaultdict(lambda:defaultdict(float))
    for (block_type, params), in config_set:
        if block_type != 'sp': continue
        use_dep_labels, label_type = params
        for path in spath_value.paths:
            path_len, key = label_path_helper(path, v2labels_dict, use_dep_labels, label_type)
            block2phi['sp', use_dep_labels, label_type, path_len][path_len, key] += 1.
    return block2phi

def label_path_helper(path, v2labels_dict, use_dep_labels, label_type):
    if label_type != '_': # decorate the path with vertex labels
        v_labels = tuple(dict2symbol(v2labels_dict[v].get(label_type, '_')) for v in path[::2])
    else: # label_type == '_': # no vertex label info
        v_labels = ()
    
    if use_dep_labels: # decorate the path with edge labels
        e_labels = path[1::2] 
    else:
        e_labels = () # no edge label info

    path_len = len(path[1::2]); assert path_len > 0
    key = v_labels + e_labels
    return path_len, key


@kproblog # FINAL FEATURES
def final_features_proc(feat_dict:feature_blocks) -> final_features:
    acc = {}
    for _, feats in feat_dict.items():
        acc = sv_add(acc, feats)
    return PolynomialSemiring.rehash(acc, nhash_m19)

def qc2facts(sentence_pkl_file_name):
    coarse_label, _fine_label, graph_list = one_pkl2dataset(sentence_pkl_file_name)
    y_i = coarse_label
    data = defaultdict(float)
    for graph in graph_list:
        for v, attr in graph.nodes(data=True):
            v = int(v)
            data[token_labels(v)] = {
                label_name: {label:1.}
                    for label_name, label in attr.items()
                        if label_name != 'vector' and label_name != 'wl'
            }
            word = attr['word']
            wl_key = word2wl_type.get(word, '_')
            data[token_labels(v)]['wl'] = {wl_key:1.}

        for v, w, attr in graph.edges(data=True):
            v, w = map(int, [v, w])
            dep_rel_label, = symbols(attr['label'])
            data[dep_rel(v, w)] = {dep_rel_label:1.}

    return y_i, data

# GENERATE CONFIGURATIONS

def bow_config_gen(label_types):
    for i in range(0, len(label_types)+1):
        for label_types_subset in itertools.combinations(label_types, i):
            yield [('bow', (lt,)) for lt in  label_types_subset]

def sp_config_gen(label_types):
    for i in range(0, len(label_types)+1):
        for label_types_subset in itertools.combinations(label_types, i):
            yield [('sp', (lt != 'lemma' and lt != 'word', lt)) for lt in  label_types_subset]

def config_gen():
    label_types = ['word', 'pos', 'lemma']
    for bow, sp in itertools.product(bow_config_gen(label_types), sp_config_gen(label_types + ['_'])):
        t = bow + sp
        if t:
            yield t

def timeout_handler(signum, frame):
    raise Exception("end of time")

def parametric_extraction(configuration_set):    
    with TimeContext("EXTRACTION"):
        train_pkl_file_name_list = glob.glob('data/qc/pkl_graphs/train/*.pkl')
        test_pkl_file_name_list = glob.glob('data/qc/pkl_graphs/test/*.pkl')

        train_y_list, train_feat_list = extract_subset_parallel(
            kproblog,
            query=final_features,
            dataset2facts_hook=qc2facts,
            configuration_set=configuration_set,
            examples_list=train_pkl_file_name_list,
            subset_size=350,
            n_jobs=N_JOBS
        )

        test_y_list, test_feat_list = extract_subset_parallel(
            kproblog,
            query=final_features,
            dataset2facts_hook=qc2facts,
            configuration_set=configuration_set,
            examples_list=test_pkl_file_name_list,
            subset_size=35,
            n_jobs=N_JOBS
        )
        
        obj2id = Obj2Id()
        train_feat_list = [PolynomialSemiring.rehash(feat, obj2id) for feat in train_feat_list]
        test_feat_list = [PolynomialSemiring.rehash(feat, obj2id) for feat in test_feat_list]
                
        train_sparse_features = SparseFeatures.from_y_and_feats(train_y_list, train_feat_list, max_feature=np.inf)
        y_train, X_train = train_sparse_features.get_yX()
        max_feature = X_train.shape[1]
        test_sparse_features = SparseFeatures.from_y_and_feats(test_y_list, test_feat_list, max_feature=max_feature)
        y_test, X_test = test_sparse_features.get_yX(max_feature)

    CLASSIFIER_SEED = 123
    KFOLD_SEED = 124
    
    # C_list = np.logspace(0, 3, 4)
    # C_list = np.logspace(2, 5, 4)
    C_list = [10000.]
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(60) # 1 minute
    
    try:
        clf = model_selection(
            C_list, X_train, y_train,
            params = dict(
                dual=False,
                multi_class='ovr',
                random_state=CLASSIFIER_SEED,
            ),
            kfold_seed=KFOLD_SEED,
            verbose_flag=True
        )
        clf.fit(X_train, y_train)

        y_pred_train = clf.predict(X_train)
        y_pred_test = clf.predict(X_test)
        acc_train = accuracy_score(y_train, y_pred_train)
        acc_test = accuracy_score(y_test, y_pred_test)

        print("FINAL LEARNING train acc: {:.1f}% acc test: {:.1f}%".format(acc_train*100., acc_test*100.))
    except Exception as msg:
        print("FINAL TIMEOUT", msg)

def main():
    PLOT_FLAG = True
    if PLOT_FLAG:
        for configuration_set in config_gen():
            print('CONFIGURATION_SET', configuration_set)
            parametric_extraction(configuration_set)
    else:
        configuration_set = {
            ('bow', ('word',)),
            ('bow', ('lemma',)),
            ('bow', ('pos',)),
            ('sp', (True, 'wl')),
            ('sp', (True, 'pos')),
            ('sp', (False, 'lemma')),
            ('sp', (True, '_'))
        }
        parametric_extraction(configuration_set)

if __name__ == '__main__':
    main()
