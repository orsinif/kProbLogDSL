import networkx as nx
import functools 
import time

def stratify_dag(dag):
    vseq = nx.topological_sort(dag)
    v2stratum_id = {v:0 for v in vseq}
    for v in vseq:
        v2stratum_id[v] = max([v2stratum_id[w] for w, v_ in dag.in_edges(v)], default=-1) + 1
    
    stratum_id_list = sorted(set(v2stratum_id.values()))
    assert all((i == stratum_i) for i, stratum_i in enumerate(stratum_id_list))
    
    strata = [[] for i in stratum_id_list]
    for v, stratum_id in v2stratum_id.items():
        strata[stratum_id].append(v)
    return strata

def make_relevant_digraph(digraph, atom_set):
    relevant_atom_set = functools.reduce(
        set.union,
        (nx.ancestors(digraph, a) for a in atom_set),
        set(atom_set)
    )
    return digraph.subgraph(relevant_atom_set)


class TimeContext(object):
    def __init__(self, ctx_name):
        self.ctx_name = ctx_name
    
    def __enter__(self):
        print("Starting {}.".format(self.ctx_name))
        self.time_a = time.time()
        return self
    
    def __exit__(self, *args, **kwargs):
        time_b = time.time()
        delta_t = time_b - self.time_a
        print("{} ellapsed time {:.3f} seconds".format(self.ctx_name, delta_t))

