from .common import split_in_blocks

def qc2data(graph_list):
    data = defaultdict(float)
    for graph in graph_list:
        v_list = []
        for v, attr in graph.nodes(data=True):
            v = int(v)
            v_list.append(v)
            data[token_labels(v)] = {
                label_name: {label:1.}
                    for label_name, label in attr.items()
                        if label_name != 'vector' and label_name != 'wl'
            }
            word = attr['word']
            wl_key = word2wl_type.get(word, '_')
            data[token_labels(v)]['wl'] = {wl_key:1.}

        v_list.sort()
        for word_i, word_j in zip(v_list[:-1], v_list[1:]):
            assert word_i + 1 == word_j
            data[next_word(word_i, word_j)] = None
        
        for v, w, attr in graph.edges(data=True):
            v, w = map(int, [v, w])
            dep_rel_label, = symbols(attr['label'])
            data[dep_rel(dep_rel_label, v, w)] = None

    return data


def extract_subset(dataset2facts_hook, configuration_set, pkl_file_name_list):
    feat_list = []
    y_list = []

    for sentence_pkl_file_name in pkl_file_name_list:
        coarse_label, _fine_label, graph_list = one_pkl2dataset(sentence_pkl_file_name)
        data_i = dataset2facts_hook(graph_list)
        data_i[config] = configuration_set # CONFIG ATOM
        with TimeContext("FEATURE EXTRACTION"):
            feats_i = feature_extraction(kproblog, data_i, final_features) #spath_features(H, V, W))
        y_i = coarse_label
        y_list.append(y_i)
        feat_list.append(feats_i)

    return y_list, feat_list

def extract_subset_parallel(dataset2facts_hook, configuration_set, pkl_file_name_list, subset_size):
    y_list = []
    feat_list = []
    parallel_it = Parallel(n_jobs=N_JOBS)(
        delayed(extract_subset)(dataset2facts_hook, configuration_set, pkl_file_name_sublist)
            for pkl_file_name_sublist in split_in_blocks(pkl_file_name_list, subset_size)
    )
    for y_list_i, feat_list_i in parallel_it:
        y_list += y_list_i
        feat_list += feat_list_i
    return y_list, feat_list

def one_pkl2dataset(sentence_pkl_file_name):
    with open(sentence_pkl_file_name, 'rb') as sentence_pkl_file:
        fine_label, graph_list = pickle.load(sentence_pkl_file)
        coarse_label, *_ = fine_label.split(':')
    return coarse_label, fine_label, graph_list


def get_yX(dataset2logic_hook, configuration_set, pkl_file_name_list, subset_size, max_feature=np.inf):
    # y_list, feat_list = extract_subset(configuration_set, pkl_file_name_list)
    y_list, feat_list = extract_subset_parallel(dataset2logic_hook, configuration_set, pkl_file_name_list, subset_size)
    # CREATE MATRIX
    i_list = []
    j_list = []
    value_list = []
    for sentence_i, feats_i in enumerate(feat_list):
        for key_j, value in feats_i.items():
            if key_j < max_feature:
                i_list.append(sentence_i)
                j_list.append(key_j)
                value_list.append(value)
    
    y = np.array(y_list)
    if np.isinf(max_feature):
        X = sp.csr_matrix((value_list, (i_list, j_list)))
    else:
        N = max(i_list) + 1
        X = sp.csr_matrix((value_list, (i_list, j_list)), shape=(N, max_feature))
    return y, X
