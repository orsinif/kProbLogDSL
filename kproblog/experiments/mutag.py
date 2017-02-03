from .common import VLABEL, ELABEL
from scipy.io import loadmat
import networkx as nx

MUTAG_MAT_FILE_NAME = './data/MUTAG.mat'

def load_mutag():
    data = loadmat(MUTAG_MAT_FILE_NAME)
    # print(data.keys())
    y = data['lmutag'].reshape((-1,))
    # print('y', y.shape)
    N, = y.shape

    for i in range(N):
        graph = nx.Graph()
        molecule = data['MUTAG'][0, i]
        node_labels = list(molecule['nl'][0,0][0].reshape((-1,)))
        for node_id, node_label in enumerate(node_labels):
            graph.add_node(node_id, **{VLABEL:int(node_label)})

        edge_list = list(molecule['el'][0,0][0])

        for v, w, elabel in edge_list:
            graph.add_edge(v-1, w-1, **{ELABEL:int(elabel)})
        # print('y[i]', i, y[i])
        yield y[i], graph
