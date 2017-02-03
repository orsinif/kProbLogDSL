from collections import defaultdict
from itertools import islice
import sys
import numpy as np
import scipy.sparse as sp
from joblib import delayed, Parallel

from kproblog import Term, KProbLog, symbols
from kproblog.core import term_to_string
from kproblog.experiments.bursi_io import FactParser
from kproblog.experiments.common import VLABEL, ELABEL, extract_subset_parallel, SparseFeatures
from kproblog.semirings import VoidMonoid, PolynomialSemiring, SetMonoid, MultisetMonoidOfMonoids, Meta, ShortestPathSemiring
from kproblog.semirings.utils import block_normalize_sum_normalize, dict2symbol, dict2tuple, nhash_m13, nhash_m17, nhash_m19, Obj2Id
from kproblog.utils import TimeContext


N_JOBS = 16

H_SP_MAX = 2
H_MAX_ITER = 1
# DEBUG_FLAG = True
DEBUG_FLAG = False

kproblog = KProbLog(debug_flag=DEBUG_FLAG)

V, W, U, H, H_SP = symbols('V, W, U, H, H_SP')
vertex, edge, edge_asymm, spath, labeled_edge, edge_sp = symbols('vertex, edge, edge_asymm, spath, labeled_edge, edge_sp')
wl, wl_multiset = symbols('wl, wl_multiset')
bow_features, features, normalized_features, feature_blocks = symbols('bow_features, features, normalized_features, feature_blocks')
spath_features, v2wl = symbols('spath_features, v2wl')
meta, config = symbols('meta, config')

kproblog.declare_destructive_many({
    PolynomialSemiring(): [
        vertex/1,
        wl/2,
        wl_multiset/2,
        edge/2,
        edge_asymm/2,
        normalized_features/0,
    ],
    MultisetMonoidOfMonoids(PolynomialSemiring()):[
        v2wl/1,
        spath_features/0,
        bow_features/0,
        features/0,
        feature_blocks/0,
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
        spath/3,
        edge_sp/2,
    ]
})

def id_hook(value):
    return PolynomialSemiring.f_id(value, nhash_m19)

@kproblog
def wl_proc0(vlabel:vertex(V)) -> wl(0, V):
    return id_hook(vlabel)

@kproblog
def wl_mult(wl_label:wl(H, W), _:edge(V, W)) -> wl_multiset(H, V):
    return wl_label

@kproblog
def wl_proc1(_:(0 < H) and (H <= H_MAX_ITER), wl_label_old:wl(H-1, V) , msgs:wl_multiset(H-1, V)) -> wl(H, V):
    key = dict2symbol(wl_label_old), dict2tuple(msgs)
    return id_hook({key:1.})

@kproblog
def v2wl_proc(wl_value:wl(H, V), info:meta) -> v2wl(H):
    h_, v = info['wl_value'].args
    return {v: wl_value}

@kproblog
def symm0(elabel:edge_asymm(V, W)) -> edge(V, W):
    return elabel

@kproblog
def symm1(elabel:edge_asymm(W, V)) -> edge(V, W):
    return elabel

@kproblog
def cast_to_shortest_path(edge_value:edge(V, W), info:meta) -> edge_sp(V, W):
    v, w = info['edge_value'].args
    edge_label, = edge_value.keys()
    return ShortestPathSemiring.create_from_edge_value(v, w, edge_label=edge_label) # XXX EDGE LABEL HERE

@kproblog
def sp_proc0(edge_value:edge_sp(V, W), info:meta) -> spath(1, V, W):
    return edge_value

@kproblog
def sp_proc1(edge_value:edge_sp(V, U), sp_value:spath(H-1, U, W), _:V != W and 2 <= H and H <= H_SP_MAX, info:meta) -> spath(H, V, W):
    # print('SPATH:',  info['return'])
    return edge_value * sp_value

@kproblog
def decorate_paths_proc(spath_value:spath(H_SP, V, W), v2wl_dict:v2wl(H), info:meta) -> spath_features:
    h, = info['v2wl_dict'].args
    block2phi = defaultdict(lambda:defaultdict(float))
    for path in spath_value.paths:
        v_labels = tuple(dict2symbol(v2wl_dict[v]) for v in path[::2])
        e_labels = path[1::2]
        path_len = len(e_labels); assert path_len > 0
        key = v_labels + e_labels
        block2phi['sp', path_len, h][path_len, h, key] += 1.
    return dict(block2phi)

@kproblog
def bow_features_block_proc(wl_label:wl(H, V), info:meta) -> bow_features:
    h, v_ = info['wl_label'].args
    block2phi = defaultdict(lambda:defaultdict(float))
    for key, value in wl_label.items():
        assert value == 1.
        block2phi['wl', 0, h][0, h, key] += 1.
    return dict(block2phi)

@kproblog
def features_bow_proc(block2phi:bow_features) -> feature_blocks:
    return block2phi

@kproblog
def features_sp_proc(block2phi:spath_features) -> feature_blocks:
    return block2phi

@kproblog
def features_proc(block2phi:feature_blocks) -> normalized_features:
    return block_normalize_sum_normalize(block2phi) # XXX taken from QC

def identity(x): return x

def main():
    N_LIMIT = None
    EXT_PL_FILE_NAME = 'data/klog/bursi_ext.pl'

    fact_parser = FactParser()
    fact_it = fact_parser.parse_interpretations_gen(EXT_PL_FILE_NAME)
    examples_list = list(islice(fact_it, N_LIMIT))
    
    with TimeContext("EXTRACTION"):
        ys, feat_list = extract_subset_parallel(
            kproblog,
            normalized_features,
            identity,
            {},
            examples_list,
            # subset_size=136,
            subset_size=68,
            n_jobs=32
        )
    
        obj2id = Obj2Id()
        feat_list = [PolynomialSemiring.rehash(feat, obj2id) for feat in feat_list]

        sparse_features = SparseFeatures.from_y_and_feats(ys, feat_list)
        if N_LIMIT is None:
            h5_file_name = 'kproblog_bursi_H_MAX_ITER_{}_H_SP_MAX_{}_new.h5'.format(H_MAX_ITER, H_SP_MAX)
        else:
            h5_file_name = 'kproblog_bursi_H_MAX_ITER_{}_H_SP_MAX_{}_limit_{}_new.h5'.format(H_MAX_ITER, H_SP_MAX, N_LIMIT)
        
        sparse_features.save_hdf5(h5_file_name)

if __name__ == '__main__':
    main()