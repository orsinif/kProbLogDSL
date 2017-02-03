from kproblog.experiments.common import SparseFeatures
import numpy as np
from matplotlib import pyplot as plt


def load_stuff(h5_file_name, perm=None):
    spm = SparseFeatures.from_hdf5(h5_file_name)
    y, X = spm.get_yX()
    if perm is None:
        perm = list(range(y.shape[0]))
        perm.sort(key=lambda i: y[i])
        perm = np.array(perm)
    K = X.dot(X.T).toarray()
    K = K[perm][:,perm]
    return y, K, perm

def main():
    h5_file_name1 = "kproblog_mutag_H_MAX_ITER_1___v1.h5"
    h5_file_name2 = "kproblog_mutag_H_MAX_ITER_1___v2.h5"
    
    y1, K1, perm = load_stuff(h5_file_name1, perm=None)
    y2, K2, _ = load_stuff(h5_file_name2, perm=perm)
    
    delta_K = abs(K2-K1)
    print("min/max", delta_K.min(), delta_K.max())
    
    assert (y1 == y2).all()


    fig, axes = plt.subplots(nrows=1, ncols=3)
    fig.add_subplot(1,3,1)
    plt.imshow(K1, interpolation="nearest")
    fig.add_subplot(1,3,2)
    plt.imshow(K2, interpolation="nearest")
    fig.add_subplot(1,3,3)
    
    plt.imshow(delta_K, interpolation="nearest")

    plt.show()
    
    err = ((K1 - K2)**2).sum()
    print('err', err)


if __name__ == '__main__':
    main()
