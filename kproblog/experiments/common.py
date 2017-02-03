from .. import symbols
from ..utils import TimeContext
from collections import defaultdict
from joblib import Parallel, delayed
import numpy as np
import scipy.sparse as sp

import glob, h5py, pickle, sys

from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import LinearSVC, SVC

from kproblog import symbols

config, = symbols('config')

VLABEL='vlabel'
ELABEL='elabel'

N_JOBS = 16 # FIXME no global vars thank you

def feature_extraction(kproblog, data, query):
    with TimeContext("GROUND_PROGRAM"):
        ground_program = kproblog.ground(query, data)
    executable = ground_program.compile()
    query_result = dict(executable.query().items())
    key, = query_result
    final_features_value, = query_result.values()
    return final_features_value

def model_selection(C_list, X, y, params, kfold_seed, verbose_flag=False, auroc_flag=False):
    CLF_CLASS = LinearSVC
    C_list = list(C_list)
    if len(C_list) > 1:
        score_C_list = []
        for C in C_list:
            if verbose_flag:
                print('\tvalid C', C)
            skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=kfold_seed)
        
            y_valid_all = []
            y_pred_valid_all = []
            for fold_i, (train_index, valid_index) in enumerate(skf.split(X, y), 1):
                if verbose_flag:
                    print('\t\tfold', fold_i)
                X_train, X_valid = X[train_index], X[valid_index]
                y_train, y_valid = y[train_index], y[valid_index]
                clf = CLF_CLASS(C=C, **params)
                if auroc_flag:
                    clf = CalibratedClassifierCV(clf, method='sigmoid', cv=3)
                
                clf.fit(X_train, y_train)
                if auroc_flag:
                    y_pred_valid = clf.predict_proba(X_valid)[:,1]
                else:
                    y_pred_valid = clf.predict(X_valid)
                    
            
                y_valid_all.append(y_valid)
                y_pred_valid_all.append(y_pred_valid)
            
        
            y_valid = np.concatenate(y_valid_all)
            y_pred_valid = np.concatenate(y_pred_valid_all)
            
            if auroc_flag:
                acc_valid = roc_auc_score(y_valid, y_pred_valid)
            else:
                acc_valid = accuracy_score(y_valid, y_pred_valid)
            if verbose_flag:
                if auroc_flag:
                    print('\tvalid auroc: {:.3f}%'.format(acc_valid))                    
                else:
                    print('\tvalid acc: {:.1f}%'.format(acc_valid*100.))
            score_C_list.append((acc_valid, C))
    
        _, C_best = max(score_C_list)
        print('\tBEST C:', C_best)
    else:
        assert len(C_list) == 1
        C_best = C_list[0]
    
    
    res_clf = CLF_CLASS(C=C_best, **params)
    if auroc_flag:
        res_clf = CalibratedClassifierCV(res_clf, method='sigmoid', cv=3)
    return res_clf


# CODE FOR PARALLELIZATION
def split_in_blocks(l, block_size):
    i = 0
    block = l[i:i+block_size]
    while True:
        if block:
            yield block
            i += block_size
            block = l[i:i+block_size]
        else:
            break

def extract_subset(kproblog, query, dataset2facts_hook, configuration_set, examples_list):
    feat_list = []
    y_list = []
    for example in examples_list:
        y_i, data_i = dataset2facts_hook(example)
        data_i[config] = configuration_set # CONFIG ATOM
        with TimeContext("FEATURE EXTRACTION"):
            feats_i = feature_extraction(kproblog, data_i, query)
        y_list.append(y_i)
        feat_list.append(feats_i)
    return y_list, feat_list

def extract_subset_parallel(kproblog, query, dataset2facts_hook, configuration_set, examples_list, subset_size, n_jobs):
    y_list = []
    feat_list = []
    parallel_it = Parallel(n_jobs)(
        delayed(extract_subset)(kproblog, query, dataset2facts_hook, configuration_set, examples_sublist)
            for examples_sublist in split_in_blocks(examples_list, subset_size)
    )
    for y_list_i, feat_list_i in parallel_it:
        y_list += y_list_i
        feat_list += feat_list_i
    return y_list, feat_list


class SparseFeatures(object):
    def __init__(self, y_list, i_list, j_list, value_list):
        self.y_list = y_list
        self.i_list = i_list
        self.j_list = j_list
        self.value_list = value_list

    def save_hdf5(self, h5_file_name):
        print('creating', h5_file_name, '...')
        with h5py.File(h5_file_name, 'w') as h5data:
            h5data.create_dataset('y', data=self.y_list)
            h5data.create_dataset('value_list', data=self.value_list)
            h5data.create_dataset('i_list', data=self.i_list)
            h5data.create_dataset('j_list', data=self.j_list)

    def get_yX(self, max_feature=np.inf):
        y = np.array(self.y_list)
        if np.isinf(max_feature):
            X = sp.csr_matrix((self.value_list, (self.i_list, self.j_list)))
        else:
            N = max(self.i_list) + 1
            X = sp.csr_matrix((self.value_list, (self.i_list, self.j_list)), shape=(N, max_feature)).toarray()
        return y, X
    
    def from_y_and_feats(y_list, feat_list, max_feature=np.inf):
        y_list = np.array(y_list)
    
        i_list = []
        j_list = []
        value_list = []
        for i, feats_i in enumerate(feat_list):
            print('example', i); sys.stdout.flush()
            for key_j, value in feats_i.items():
                if key_j < max_feature:
                    i_list.append(i)
                    j_list.append(key_j)
                    value_list.append(value)
        return SparseFeatures(y_list, i_list, j_list, value_list)
    
    def from_hdf5(h5_file_name):
        with h5py.File(h5_file_name, 'r') as h5data:
            y_list = h5data['y'].value
            i_list = h5data['i_list'].value
            j_list = h5data['j_list'].value
            value_list = h5data['value_list'].value
        return SparseFeatures(y_list, i_list, j_list, value_list)
