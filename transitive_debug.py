import numpy as np
from kproblog import Term, KProbLog, symbols
from kproblog.semirings import RealSemiring, TropicalSemiring
# from kproblog.semirings.utils import nhash_m19
from kproblog.semirings.utils import Obj2Id
from kproblog.utils import TimeContext
from kproblog.core import term_to_string

obj2id = Obj2Id()

MAX_ITER = 3

DEBUG_FLAG = False

kproblog = KProbLog(debug_flag=DEBUG_FLAG)

V, W, U = symbols('V, W, U')
edge, path = symbols('edge, path')

kproblog.declare_additive_many({
    # RealSemiring(): [
    TropicalSemiring(): [
        edge/2,
        path/2,
    ]
})


@kproblog
def path1(w:edge(V, W)) -> path(V, W):
    return w

@kproblog
def path2(w1:edge(V, U), w2:path(U, W)) -> path(V, W):
    return TropicalSemiring().prod([w1, w2])

def main():
    data = {
        edge(1, 2): 1.,
        edge(2, 3): 1,
        edge(3, 4): 1.,
        edge(4, 5): 1.,
    }
    query = path(1, W)
    
    with TimeContext("GROUND_PROGRAM"):
        ground_program = kproblog.ground(query, data)

    if DEBUG_FLAG:
        print(ground_program.nodes())

    executable = ground_program.compile()

    if DEBUG_FLAG:
        print(80 * '=')
        print(80 * '=')
        print('STRATA')
        for stratum in executable.strata:
            print(stratum)
            stratum._monoid_deco_gen(stratum.acyclic, ground_program)
            print()
        print(80 * '=')
        print(80 * '=')

    for atom, weight in executable.query().items():
        print(atom, ":", weight)

if __name__ == '__main__':
    main()