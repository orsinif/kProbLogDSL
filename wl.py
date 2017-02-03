import numpy as np
from kproblog import Term, KProbLog, symbols
from kproblog.semirings import VoidMonoid, PolynomialSemiring
# from kproblog.semirings.utils import nhash_m19
from kproblog.semirings.utils import Obj2Id
from kproblog.utils import TimeContext
from kproblog.core import term_to_string

obj2id = Obj2Id()

MAX_ITER = 3

DEBUG_FLAG = False

kproblog = KProbLog(debug_flag=DEBUG_FLAG)

V, W, H = symbols('V, W, H')
vertex, edge, edge_asymm = symbols('vertex, edge, edge_asymm')
wl_color, wl_color_multiset, succ = symbols('wl_color, wl_color_multiset, succ')
wl_feat_h_iter, wl_feat = symbols('wl_feat_h_iter, wl_feat')

kproblog.declare[PolynomialSemiring()](
    vertex/1,
    wl_color/2,
    wl_color_multiset/2
)

kproblog.declare[VoidMonoid()](
    edge/2,
    edge_asymm/2
)
    
if DEBUG_FLAG:
    print('=' * 80)

    for k, v in kproblog.pred_signature2monoid.items():
        print(k)
        print('\t', v)
        print()

    print('=' * 80)

def multiset_id(multiset):
    return obj2id(tuple(sorted(multiset.items())))

@kproblog
def connectivity1(w: edge_asymm(V, W)) -> edge(V, W):
    pass

@kproblog
def connectivity2(_: edge_asymm(W, V)) -> edge(V, W):
    pass

@kproblog
def messages(_none:edge(V, W), label:wl_color(H, W)) -> wl_color_multiset(H, V):
    return label

f_id = PolynomialSemiring.f_id
union = PolynomialSemiring().sum

@kproblog
def wl_color_rule1(v_label:vertex(V)) -> wl_color(0, V):
    return PolynomialSemiring.f_id(v_label, obj2id)

@kproblog
def wl_color_rule2(_1:1 <= H, _2:H <= MAX_ITER, v_color:wl_color(H-1, V), color_multiset:wl_color_multiset(H-1, V)) -> wl_color(H, V):
    return f_id(union([v_color, f_id(color_multiset, obj2id)]), obj2id)


def main():
    data = {
        vertex(1): {'pink':1.},
        vertex(2): {'blue':1.},
        vertex(3): {'blue':1.},
        vertex(4): {'blue':1.},
        vertex(5): {'blue':1.},
        edge_asymm(1, 2): None,
        edge_asymm(1, 3): None,
        edge_asymm(2, 4): None,
        edge_asymm(3, 4): None,
        edge_asymm(4, 5): None,
    }
    query = wl_color(MAX_ITER, V)
    
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