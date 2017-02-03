import functools

from ..core import symbols


def get_tokens(s):
    s = "".join(s.split())
    ch_list = ['(', ')', ',', '.']
    l = {s}
    for ch in ch_list:
        l = functools.reduce(set.union, [set(ss.split(ch)) for ss in l])
    return list(filter(bool, l))

def parse_term(term_str):
    # XXX very dirty trick implementation
    tokens = [token for token in get_tokens(term_str) if not token[0].isdigit()]

    cmd = "{} = symbols('{}')".format(", ".join(tokens), " ".join(tokens))
    exec(cmd)
    return eval(term_str)

