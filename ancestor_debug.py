import numpy as np
from kproblog import Term, KProbLog, symbols
from kproblog.semirings import RealSemiring, Meta

# TODO check semirings between strata
# TODO implement cycle detection
# TODO implement cyclic Tp-operator


kproblog = KProbLog(debug_flag=True)

X, Y, Z = symbols('X Y Z')
father, ancestor = symbols('father ancestor')
meta, = symbols('meta')
abraham, esau, isaac, jacob = symbols('abraham esau isaac jacob')

kproblog.declare[RealSemiring(2)](
    ancestor/2,
    father/2
)
kproblog.declare[Meta()](
    meta/0
)

@kproblog
def meta1(w_p: father(X, Y)) -> ancestor(X, Y):
    return np.exp(w_p)


def meta2(w_a, w_p) :
    return w_a * w_p


@kproblog
def meta2(w_a: ancestor(X, Z), w_p: father(Z, Y), info:meta) -> ancestor(X, Y):
    print("INFO:", info)
    return w_a * w_p

def main():
    data = {
        father(abraham, isaac): np.array([0.5, 0.1]),
        father(isaac, jacob): np.array([0.1, 0.3]),
        father(isaac, esau): np.array([0.2, 0.4])
    }
    query = ancestor(abraham, X)
    ground_program = kproblog.ground(query, data)
    executable = ground_program.compile()
    for atom, weight in executable.query().items():
        print(atom, ":", weight)

if __name__ == '__main__':
    main()
    
