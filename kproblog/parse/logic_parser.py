import re

# from ..core import Term

class LogicTerm(object):
    def __init__(self, functor, *args):
        assert isinstance(functor, str)
        assert all(isinstance(arg, LogicTerm) for arg in args)
        self.functor = functor
        self.args = tuple(args)
    
    def __hash__(self):
        return hash((self.functor, self.args))

    def __eq__(self, other):
        return (self.functor, self.args) == (other.functor, other.args)
    
    @property
    def arity(self):
        return len(self.args)
    
    @property
    def signature(self):
        return self.functor, self.arity
    
    def __repr__(self):
        if self.functor == '[]':
            return '[{}]'.format(', '.join(map(str, self.args)))
        else:
            if self.args:
                return "{}({})".format(self.functor, ', '.join(map(repr, self.args)))
            else:
                return "{}".format(self.functor)

def tokenize(s):
    return re.findall("\.|,|[\'\w\-]+|\[|\]|\(|\)", s)

def is_identifier(s):
    return s not in ".,()[]"

def parse_atom(tokens):
    if tokens[-1] != '.':
        raise ValueError
    return parse_term(tokens[:-1])

def parse_term(tokens):
    if is_identifier(tokens[0]):
        if len(tokens) == 1: # 0 arity
            assert isinstance(tokens[0], str)
            return LogicTerm(tokens[0])
        else: # n-ary
            functor, bra, *arg_tokens, ket = tokens
            if not (bra == '(' and ket == ')'):
                # print('DEBUG tokens:', tokens)
                # print('DEBUG functor:', functor)
                # print('DEBUG bra:', bra)
                # print('DEBUG arg_tokens:', arg_tokens)
                # print('DEBUG ket:', ket)
                raise ValueError("parse_term error0: {}".format(tokens))
            if arg_tokens:
                args = parse_term_list(arg_tokens)
                return LogicTerm(functor, *args)
            else:
                raise ValueError("parse_term error1: {}".format(tokens))
    elif tokens[0] == '[' and tokens[-1] == ']': # list
        sqbra, *arg_tokens, sqket = tokens
        assert sqbra == '[' and sqket == ']'
        if arg_tokens:
            args = parse_term_list(arg_tokens)
            return LogicTerm('[]', *args)
        else:
            return LogicTerm('[]')
            
    else:
        raise ValueError("parse_term error2: {}".format(tokens))

def parse_term_list(tokens):
    assert tokens[-1] != ','
    for token_i, token in enumerate(tokens):
        if token == ',':
            tokens_before = tokens[:token_i]
            tokens_after = tokens[token_i+1:]
            try:
                term = parse_term(tokens_before)
                term_list = parse_term_list(tokens_after)
            except ValueError:
                continue
            return (term,) + term_list
    return (parse_term(tokens),)
