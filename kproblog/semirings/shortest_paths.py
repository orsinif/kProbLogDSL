from itertools import groupby
from .semirings import CommutativeMonoid
import numpy as np
    
    
# def make_ShortestPathSemiringElem(paths):
#     new_paths = set()
#     min_path_len = np.inf
#     for path in paths:
#         path_len = len(path)
#         if path_len < min_path_len:
#             min_path_len = path_len
#             new_paths = set()
#             new_paths.add(path)
#         elif path_len == min_path_len:
#             new_paths.add(path)
#         # else: path_len > min_path_len:
#         #     pass
#     return new_paths, min_path_len
            
class ShortestPathSemiringElem(object):
    def __init__(self, paths, path_len):
        self.paths = paths
        self.path_len = path_len
        assert not set(map(len, self.paths)) or set(map(len, self.paths)) == {path_len}, "{} vs {}".format(set(map(len, self.paths)), {path_len})

    def __eq__(self, other):
        return self.path_len == other.path_len and self.paths == other.paths
    
    def __mul__(self, other):
        path_set = set()
        for path1 in self.paths:
            for path2 in other.paths:
                if path1[-1] == path2[0]:
                    path_set.add(path1[:-1] + path2)
        return ShortestPathSemiringElem(path_set, self.path_len + other.path_len - 1)
        
    def __add__(self, other):
        if self.path_len == other.path_len:
            return ShortestPathSemiringElem(self.paths.union(other.paths), self.path_len)
        elif self.path_len < other.path_len:
            return self
        else: # self.path_len > other.path_len
            return other

    def __repr__(self):
        return "SPElem([{}])".format(", ".join(map(str, self.paths)))
        

class ShortestPathSemiring(CommutativeMonoid):
    @property
    def zero(self):
        return ShortestPathSemiringElem(set(), np.inf)
    
    @property
    def one(self):
        return ShortestPathSemiringElem(set(()), 0)
    
    def sum(self, l):
        acc = self.zero
        for elem in l:
            assert isinstance(elem, ShortestPathSemiringElem), (type(elem), elem)
            acc = acc + elem
        return acc
    
    def prod(self, l):
        acc = self.one
        for elem in l:
            acc = acc * elem
        return acc
    
    def parse_value(self, atom, value):
        raise NotImplementedError
    
    def parse_function_arg(self, atom, value):
        # print("NotImplementedError: atom=", atom, "value=", value)
        # raise NotImplementedError
        return value
    
    def create_from_edge_value(v, w, edge_label=None):
        path = (v, edge_label, w)
        return  ShortestPathSemiringElem(paths = {path}, path_len = len(path))