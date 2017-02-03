from kproblog.experiments.common import SparseFeatures
from kproblog.experiments.common import model_selection

from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold

import glob
import numpy as np
import argparse

KFOLD_SEED = 124

parser = argparse.ArgumentParser(description='run 10 times 10 fold cv.')
parser.add_argument('h5files', type=str, nargs='+')
parser.add_argument('--auroc', action='store_true')

args = parser.parse_args()
AUROC_FLAG = args.auroc

# for h5_file_name in glob.iglob('*.h5'):
for h5_file_name in args.h5files:
    print('=' * 80)
    print('=' * 80)
    print('h5_file_name', h5_file_name)
    
    sparse_features = SparseFeatures.from_hdf5(h5_file_name)
    y, X = sparse_features.get_yX()
    print('y.shape', y.shape)
    print('X.shape', X.shape)
    print('=' * 80)

    C_list = [1]
    C_list = np.logspace(-0.5, 0.5, 5)
    
    # C_list = np.logspace(-3, 3, 3)

    random_state = np.random.RandomState(123)

    acc_list = []

    for time_i in range(10):
        skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=random_state)
        y_test_all = []
        y_pred_all = []
        for train_index, test_index in skf.split(X, y):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            clf = model_selection(C_list, X_train, y_train, params={}, kfold_seed=KFOLD_SEED, auroc_flag=AUROC_FLAG)
            clf.fit(X_train, y_train)
            if AUROC_FLAG:
                y_pred_test = clf.predict_proba(X_test)[:,1]
            else:
                y_pred_test = clf.predict(X_test)
            y_test_all.append(y_test)
            y_pred_all.append(y_pred_test)

        y_test_all = np.concatenate(y_test_all)
        y_pred_all = np.concatenate(y_pred_all)
        if AUROC_FLAG:
            test_acc = roc_auc_score(y_test_all, y_pred_all)
        else:
            test_acc = accuracy_score(y_test_all, y_pred_all)
        acc_list.append(test_acc)
        print(test_acc)
        if AUROC_FLAG:
            print("\t({}) test auroc : {:.3f}".format(time_i, test_acc))
        else:
            print("\t({}) test acc : {:.1f}%".format(time_i, test_acc*100))
    
    if AUROC_FLAG:
        print('avg auroc {:.3f} +/- {:.3f}'.format(np.mean(acc_list), np.std(acc_list)))
    else:
        print('avg acc {:.1f}% +/- {:.1f}%'.format(np.mean(acc_list)*100., np.std(acc_list)*100.))
