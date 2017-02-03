import functools
from collections import defaultdict
import hashlib, zlib

def dict2tuple(d):
    return tuple(sorted(d.items()))
    
def set2tuple(s):
    return tuple(sorted(s))

def dict2symbol(d):
    (key, val), = d.items()
    if val != 1: raise ValueError("value = {}".format(val))
    return key

def sv_add(a, b):
    res = defaultdict(float)
    res.update(a)
    for k, v in b.items():
        res[k] += v
    return dict(res)

def sv_div(a, scalar):
    return {k:v/scalar for k, v in a.items()}

def sv_norm2(a):
    return sum(v*v for v in a.values()) # FIXME BUG HERE. Square root is missing, but this makes things work better.

def sv_normalize(a):
    n = sv_norm2(a)
    if abs(n) > 1e-6:
        return sv_div(a, n)
    else:
        return {}
        
def block_sum(block2sv):
    return functools.reduce(sv_add, block2sv.values(), {})

def block_sum_normalize(block2sv):
    return sv_normalize(functools.reduce(sv_add, block2sv.values(), {}))

def block_normalize_sum_normalize(block2sv):
    return sv_normalize(functools.reduce(sv_add, map(sv_normalize, block2sv.values()), {}))

class Obj2Id(object):
    def __init__(self):
        self.i = 0
        self.d = {}
    
    def __len__(self):
        return self.i
    
    def __getitem__(self, key):
        if key not in self.d:
            self.d[key] = self.i
            self.i += 1
        return self.d[key]

    def __call__(self, key):
        return self[key]


PRIME_M13 = 2**13-1
PRIME_M17 = 2**17-1
PRIME_M19 = 2**19-1
PRIME_M31 = 2**31-1


def hash_object(obj):
    obj_str = str(obj)
    obj_bytes = bytes(obj_str, 'utf8')
    return zlib.adler32(obj_bytes)
    # return zlib.crc32(obj_bytes)
    # return int(hashlib.md5(obj_bytes).hexdigest(), 16)

def nhash_m13(obj):
    return hash_object(obj) % PRIME_M13

def nhash_m17(obj):
    return hash_object(obj) % PRIME_M17

def nhash_m19(obj):
    return hash_object(obj) % PRIME_M19

def nhash_m31(obj):
    return hash_object(obj) % PRIME_M31


# def nhash_m13(obj):
#     h = hash(obj)
#     if h >= 0:
#         res = 2 * h
#     else:
#         res = -2 * h + 1
#     return res % PRIME_M13
#
# def nhash_m17(obj):
#     h = hash(obj)
#     if h >= 0:
#         res = 2 * h
#     else:
#         res = -2 * h + 1
#     return res % PRIME_M17
#
#
# def nhash_m19(obj):
#     h = hash(obj)
#     if h >= 0:
#         res = 2 * h
#     else:
#         res = -2 * h + 1
#     return res % PRIME_M19
#
# def nhash_m31(obj):
#     h = hash(obj)
#     if h >= 0:
#         res = 2 * h
#     else:
#         res = -2 * h + 1
#     return res % PRIME_M31

