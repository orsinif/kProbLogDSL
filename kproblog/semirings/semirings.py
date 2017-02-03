from abc import ABCMeta, abstractmethod, abstractproperty
from collections import defaultdict, namedtuple
import networkx as nx
import numpy as np
from itertools import groupby

# TODO make sure that all the monoid elements implement __eq__

class Meta(object):
    pass

class CommutativeMonoid(metaclass=ABCMeta):
    @abstractproperty
    def zero(self):
        pass

    @abstractmethod
    def sum(self, l):
        pass

    @abstractmethod    
    def parse_value(self, atom, value):
        pass
    
    @abstractmethod  # it should just returns value unless we want some sort of graphicalization
    def parse_function_arg(self, atom, value):
        pass

class CommutativeSemiring(CommutativeMonoid, metaclass=ABCMeta):
    @abstractproperty
    def one(self):
        pass

    @abstractmethod
    def prod(self, l):
        pass


class GraphMonoid(CommutativeMonoid):
    @property
    def zero(self):
        return nx.Graph()
    
    def sum(self, l):
        if l:
            return nx.compose_all(l)
        else:
            return self.zero
    
    def parse_value(self, atom, value):
        return self.term2graph(atom)
    
    def parse_function_arg(self, atom, value):
        return self.term2graph(atom)
    
    def term2graph(self, term):
        graph = nx.Graph()
        graph.add_node(term, node_type='E')
        for arg_i, arg in enumerate(term.args):
            graph.add_node(arg, node_type='R')
            graph.add_edge(term, arg, edge_type=arg_i) # TODO implement kLog roles
        return graph

class RealSemiring(CommutativeSemiring):
    def __init__(self, *shape):
        self.shape = shape

    @property
    def zero(self):
        return np.zeros(self.shape)

    @property
    def one(self):
        return np.ones(self.shape)

    def sum(self, l):
        if l:
            return np.sum(l, 0)
        else:
            return self.zero

    def prod(self, l):
        if l:
            return np.prod(l)
        else:
            return self.one

    def parse_value(self, atom, value):
        res = np.array(value)
        if res.shape != self.shape:
            raise ValueError("incorrect shape: expected {} got {}"\
                .format(self.shape, res.shape))
        return res
    
    def parse_function_arg(self, atom, value):
        return value


class MaxRplusMonoid(CommutativeSemiring):
    def __init__(self, *shape):
        self.shape = shape
    
    @property
    def zero(self):
        return np.zeros(self.shape)
    
    @property
    def one(self):
        return np.zeros(self.shape)

    def sum(self, l):
        if l:
            return np.maximum(*l)
        else:
            return self.zero

    def prod(self, l):
        if l:
            return np.sum(*l)
        else:
            return self.one

    
    def parse_value(self, atom, value):
        res = np.array(value)
        if res.shape != self.shape:
            raise ValueError("incorrect shape: expected {} got {}"\
                .format(self.shape, res.shape))
        if not (res >= 0).all():
            raise ValueError("negative elements are not allowed")
        return res
    
    def parse_function_arg(self, atom, value):
        return value


def _poly_mul(a, b):
    res = defaultdict(float)
    for k1, v1 in a.items():
        for k2, v2 in b.items():
            k_left, k_right = sorted([k1, k2])
            res[k_left + k_right] += v1 * v2
    return res


class PolynomialSemiring(CommutativeSemiring):
    @property
    def zero(self):
        return {}
    
    @property
    def one(self):
        return {():1.}

    def sum(self, l):
        res = defaultdict(float)
        for multiset in l:
            for k, v in multiset.items():
                res[k] += v
        return dict(res)

    def prod(self, l):
        if l:
            acc = self.one
            for elem in l:
                acc = _poly_mul(acc, elem)
            return acc
        else:
            return self.one
    
    def parse_value(self, atom, value):
        return {k:float(v) for k, v in value.items()}
    
    def parse_function_arg(self, atom, value):
        return value
    
    def f_id(value, hash_hook):
        return {hash_hook(tuple(sorted(value.items()))): 1.}
    
    def l2_norm(sv):
        return np.sqrt(sum(val*val for val in sv.values()))

    def l1_norm(sv):
        return np.sqrt(sum(abs(val) for val in sv.values()))
    
    def normalize_l2(sv):
        nn = PolynomialSemiring.l2_norm(sv)
        if abs(nn) > 1e-6:
            return {k:v/nn for k, v in sv.items()}
        else:
            return {}

    def rehash(d, id_hook):
        res = defaultdict(float)
        for k, v in d.items():
            res[id_hook(k)] += v
        return dict(res)
    
    def filterhash(d, id_hook, num, den):
        res = {}
        for key, value in d.items():
            key_hash = id_hook(key)
            if key_hash % den < num:
                res[key_hash] = value
        return res

class MultisetMonoidOfMonoids(CommutativeMonoid):
    def __init__(self, inner_monoid):
        self.inner_monoid = inner_monoid
    
    @property
    def zero(self):
        return {}

    @property
    def one(self):
        return {():self.inner_monoid.one}

    def sum(self, l):
        res = defaultdict(lambda: self.inner_monoid.zero) # TODO remove
        # res = {}
        for multiset in l:
            for k, v in multiset.items():
                res[k] = self.inner_monoid.sum([res[k], v])
        return dict(res)

    def prod(self, l):
        if l:
            acc = self.one
            for elem in l:
                acc = self._poly_poly_mul(acc, elem)
            return acc
        else:
            return self.one

    def _poly_poly_mul(self, acc, elem):
        res = defaultdict(lambda:self.inner_monoid.zero)
        for k1, v1 in a.items():
            for k2, v2 in b.items():
                k = sorted(k1 +k2)
                res[k] += self.inner_monoid.prod([v1, v2])
        return res

    def parse_value(self, atom, value):
        return value

    def parse_function_arg(self, atom, value):
        return value
    

class SetMonoid(CommutativeSemiring):
    @property
    def zero(self):
        return set()
    
    @property
    def one(self):
        return {(),}

    def sum(self, l):
        res = set()
        for s in l:
            res = res.union(s)
        return res

    def mul(self, a, b):
        return {a + b for ka in a for kb in b}

    def prod(self, l):
        res = self.zero
        for s in l:
            res = self.mul(res, s)
        return res

    def parse_value(self, atom, value):
        return {(elem,) for elem in value}
    
    def parse_function_arg(self, atom, value):
        return value


class VoidMonoid(CommutativeSemiring):
    @property
    def zero(self):
        return None
    
    @property
    def one(self):
        return None


    def sum(self, l):
        return None

    def prod(self, l):
        return None

    def parse_value(self, atom, value):
        if value is not None:
            raise ValueError
        return None
    
    def parse_function_arg(self, atom, value):
        return value


def test_MultisetMonoid():
    foo = PolynomialSemiring()
    values = [{'a':3, 'b':4.5}, {'a':3, 'c':5.2}]
    values = list(map(foo.parse_value, values))
    print("RES")
    print(foo.sum(values))


class TropicalSemiring(CommutativeSemiring):
    
    @property
    def zero(self):
        return np.inf
    
    @property
    def one(self):
        return 0.

    def sum(self, l):
        if l:
            return min(l)
        else:
            return self.zero

    def prod(self, l):
        if l:
            return sum(l)
        else:
            return self.one

    
    def parse_value(self, atom, value):
        assert value >= 0
        return value
    
    def parse_function_arg(self, atom, value):
        return value
