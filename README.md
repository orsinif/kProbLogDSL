# kProbLogDSL

To install kProbLog you need Python 3.5 or newer (https://www.continuum.io/downloads).

Install the following dependencies:
    
    $ python -m pip install joblib
    
    $ python -m pip install networkx
    
    $ python -m pip install h5py


Install gringo4.5 grounder:

    $ brew install gringo # on Mac OS X
    $ aptitude install gringo # on Ubuntu/Linux

Clone the kProbLog repository:

    $ git clone https://github.com/orsinif/kProbLogDSL.git
    $ cd kProbLogDSL

Make sure that the variable GRINGO_BIN_FILE_PATH in kproblog/config.py points to the gringo executable.

Launch a test:
    
    $ python wl.py

If you get a syntax error, you are probably using Python2.
If some dependencies are missing make sure you installed them for Python3

Launch kProbLog on MUTAG
    
    $ python kproblog_mutag.py
compute the accuracy
    
    $ python h5experiments.py kproblog_mutag_H_MAX_ITER_1_paper.h5

Launch kProbLog on BURSI
    
    $ python kproblog_bursi.py

compute the auroc
    
    $ python h5experiments.py kproblog_bursi_H_MAX_ITER_1_H_SP_MAX_2_new.h5 --auroc
