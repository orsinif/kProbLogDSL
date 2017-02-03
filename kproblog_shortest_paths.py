import numpy as np
from kproblog import Term, KProbLog, symbols
from kproblog.semirings import VoidMonoid, PolynomialSemiring, Meta
from kproblog.semirings import ShortestPathSemiring, ShortestPathSemiringElem
from kproblog.utils import TimeContext
from kproblog.core import term_to_string

# MAX_ITER = 3
# DEBUG_FLAG = True
DEBUG_FLAG = False

def argmin_from_edge(src, dst):
    return ArgminElem(src, dst, [(src, dst)])        

kproblog = KProbLog(debug_flag=DEBUG_FLAG)

H_MAX_ITER = 2

V, W, U, H = symbols('V, W, U, H')

vertex, edge, edge_asymm, spath = symbols('vertex, edge, edge_asymm spath')
wl, wl_multiset = symbols('wl, wl_multiset')
meta, = symbols('meta')

kproblog.declare_destructive_many({
    PolynomialSemiring():[vertex / 1],
    Meta(): [meta/0],
    VoidMonoid(): [edge/2, edge_asymm/2],
})

kproblog.declare_additive_many({
    ShortestPathSemiring():[spath/2]
})

@kproblog    
def symm0(_:edge_asymm(V, W)) -> edge(V, W):
    pass

@kproblog    
def symm1(_:edge_asymm(W, V)) -> edge(V, W):
    pass

@kproblog
def sp_proc0(ground_edge:edge(V, W), info:meta) -> spath(V, W):
    v, w = info['ground_edge'].args
    return ShortestPathSemiringElem({(v, w)})

@kproblog
def sp_proc1(sp1:spath(V, U), sp2:spath(U, W), _:V != W) -> spath(V, W):
    return sp1 * sp2

def main():
    data = {
        edge_asymm(1, 2): None,
        edge_asymm(1, 3): None,
        edge_asymm(2, 4): None,
        edge_asymm(3, 4): None,
        edge_asymm(4, 5): None,
        # edge_asymm(6, 5): None,
    }
    query = spath(V, W)
    
    with TimeContext("GROUND_PROGRAM"):
        ground_program = kproblog.ground(query, data)

    if DEBUG_FLAG:
        print(ground_program.nodes())

    executable = ground_program.compile()

    executable.pretty_print()
    if DEBUG_FLAG:
        print(80 * '=')
        print(80 * '=')
        print('STRATA')
        for stratum in executable.strata:
            stratum.pretty_print()
            stratum._monoid_deco_gen(stratum.acyclic, ground_program)
            print()
        print(80 * '=')
        print(80 * '=')
    
    print("RESULT")
    for atom, weight in executable.query().items():
        print(atom, ":", weight)

if __name__ == '__main__':
    main()


# mutag + background knowledge

