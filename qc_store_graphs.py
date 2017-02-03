import codecs
import networkx as nx
import os
from spacy.en import English
import sys

from kproblog.experiments.qc_io import Word2WL_Type, digraph_sentence2pkl

LIMIT = -1

def main():
    # PKL_FOLDER = 'data/qc/pkl_logic'
    PKL_GRAPH_FOLDER = 'data/qc/pkl_graphs'
    TRAIN_FILE_NAME = 'data/qc/train_5500.label'
    TEST_FILE_NAME = 'data/qc/TREC_10.label'
    
    for folder in PKL_GRAPH_FOLDER,:
        if not os.path.exists(folder):
            os.makedirs(folder)
        
    word2wl_type = Word2WL_Type()

    parser = English()    
    for sentence_type, sentence_list_file_name in zip(['train', 'test'], [TRAIN_FILE_NAME, TEST_FILE_NAME]):
        print('sentence_type:', sentence_type)
        
        
        sent_fold_folder = os.path.join(PKL_GRAPH_FOLDER, sentence_type)
        
        if not os.path.exists(sent_fold_folder):
            os.makedirs(sent_fold_folder)
        
        with codecs.open(sentence_list_file_name, "r", "L9") as sentence_list_file:
            print('=' * 80)
            for sentence_i, line in enumerate(sentence_list_file):
                if sentence_i == LIMIT: break
                line = line.strip()
                label, *parts = map(str, line.split())
                sentence_txt = " ".join(list(parts))
                parsed_data = parser(sentence_txt)
                sent_digraph_list = word2wl_type.parsed_data2sent_digraph_list(parsed_data)
                pkl_file_name = os.path.join(sent_fold_folder, 'sentence_{:05d}.pkl'.format(sentence_i))
                digraph_sentence2pkl(pkl_file_name, sent_digraph_list, label)
                print('.', end='')
                sys.stdout.flush()
                # logic_sentence2pkl(pkl_file_name, sent_digraph_list)
        print()


if __name__ == '__main__':
    main()
