from collections import defaultdict
from spacy.en import English
import codecs
import networkx as nx
import pickle
import numpy as np
import scipy.sparse as sp
import sys

# STORE

class Word2WL_Type(object):
    def __init__(self):
        word2types = defaultdict(set)
        for wl_type in 'food', 'mount', 'prof':
            with codecs.open('data/qc/{}'.format(wl_type), "r", "L9") as wl_file:
                for word in wl_file:
                    word = word.strip()
                    word2types[word].add(wl_type)
        self.word2wl_type = dict(word2types)
    
    def get(self, word, default_value=None):
        wl_types = tuple(sorted(self.word2wl_type.get(word, default_value)))
        return wl_types
        
    
    def parsed_data2sent_digraph_list(self, parsed_data):
        sent_digraph_list = []
        for sent in parsed_data.sents:
            sent_digraph = nx.DiGraph()
            for token in sent:
                lemma = token.lemma_
                sent_digraph.add_node(
                    token.i,
                    word=str(token),
                    pos=str(token.pos_),
                    lemma=str(token.lemma_),
                    vector=token.vector,
                    is_stop=token.is_stop,
                    wl=self.word2wl_type[lemma] if lemma in self.word2wl_type else set()
                )
            for t1 in sent:
                for t2 in t1.children:
                    sent_digraph.add_edge(int(t1.i), int(t2.i), label=str(t2.dep_))
            sent_digraph_list.append(sent_digraph)
        return sent_digraph_list


def digraph_sentence2pkl(pkl_file_name, sent_digraph_list, label):
    with open(pkl_file_name, 'wb') as pkl_file:
         pickle.dump((label, sent_digraph_list), pkl_file)


# LOAD

def one_pkl2dataset(sentence_pkl_file_name):
    with open(sentence_pkl_file_name, 'rb') as sentence_pkl_file:
        fine_label, graph_list = pickle.load(sentence_pkl_file)
        coarse_label, *_ = fine_label.split(':')
    return coarse_label, fine_label, graph_list

# NOT DECLARATIVE
# def pkl2dataset(feature_extraction, pkl_file_name_list, M=None):
#     y_coarse = []
#     y_fine = []
#     i_list = []
#     j_list = []
#     data = []
#     for sentence_i, sentence_pkl_file_name in enumerate(pkl_file_name_list):
#         coarse_label, fine_label, graph_list = one_pkl2dataset(sentence_pkl_file_name)
#         # with open(sentence_pkl_file_name, 'rb') as sentence_pkl_file:
#         #     fine_label, graph_list = pickle.load(sentence_pkl_file)
#         #     coarse_label, *_ = fine_label.split(':')
#         y_coarse.append(coarse_label)
#         y_fine.append(fine_label)
#         feat = feature_extraction.extract(graph_list)
#         for k, v in feat.items():
#             if M is None or k < M:
#                 i_list.append(sentence_i)
#                 j_list.append(k)
#                 data.append(v)
#
#     y_coarse = np.array(y_coarse)
#     y_fine = np.array(y_fine)
#     if M is None:
#         X = sp.csr_matrix((data, (i_list, j_list)))
#     else:
#         N = max(i_list) + 1
#         X = sp.csr_matrix((data, (i_list, j_list)), shape=(N, M))
#     return y_coarse, y_fine, X
