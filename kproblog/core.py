from collections import namedtuple
FACT_IDENTIFIER = 'fact'
QUERY_IDENTIFIER = 'query'


INFIX_ATOMS = {
    '==': 'keyword_eq',
    '!=': 'keyword_ne',
    '<': 'keyword_lt',
    '<=': 'keyword_le',
    '>=': 'keyword_ge',
    '>': 'keyword_gt',
}

INFIX_TERMS = {
    '+': 'keyword_add',
    '-': 'keyword_sub',
}

INFIX_OPERATORS = {}
INFIX_OPERATORS.update(INFIX_ATOMS)
INFIX_OPERATORS.update(INFIX_TERMS)

INV_INFIX_OPERATORS = {v:k for k, v in INFIX_OPERATORS.items()}

def term_to_string(arg, as_atom_flag):
    if isinstance(arg, Term):
        functor_str = str(arg.functor)
        if arg.args:
            args_str_list = [term_to_string(arg, False) for arg in arg.args]
            if functor_str in INFIX_OPERATORS:
                if len(arg.args) != 2: raise Error
                s1, s2 = args_str_list
                if functor_str in INFIX_TERMS or (functor_str in INFIX_ATOMS and as_atom_flag):
                    return "{} {} {}".format(s1, functor_str, s2)
                elif functor_str in INFIX_ATOMS and not as_atom_flag:
                    return '{}({}, {})'.format(INFIX_OPERATORS[functor_str], s1, s2)
                else:
                    raise ValueError
            else:
                args_str = ", ".join(args_str_list)
                return "{}({})".format(functor_str, args_str)
        else:
            return functor_str
    elif isinstance(arg, int):
        return str(arg)
    elif isinstance(arg, str):
        return '"{}"'.format(arg)
    else:
        print('arg', arg)
        raise ValueError


class Term(object):
    def __init__(self, functor, *args):
        assert isinstance(functor, str)
        self.functor = functor
        self.args = args
    
    def __add__(self, other):
        return Term('+', self, other)
    
    def __radd__(self, other):
        return Term('+', other, self)

    def __sub__(self, other):
        return Term('-', self, other)
    
    def __rsub__(self, other):
        return Term('-', other, self)

    def __eq__(self, other):
        return Term('==', self, other)

    def __ne__(self, other):
        return Term('!=', self, other)
            
    def __le__(self, other):
        return Term('<=', self, other)
    
    def __lt__(self, other):
        return Term('<', self, other)
    
    def __ge__(self, other):
        return Term('>=', self, other)
    
    def __gt__(self, other):
        return Term('>', self, other)

    def __matmul__(self, role):
        return RoleTerm(self, role)
        
    def strip_role(self):
        functor = self.functor
        args = []
        for arg in self.args:
            if isinstance(arg, int) or isinstance(arg, str):
                args.append(arg)
            else:
                args.append(arg.strip_role())
        return Term(functor, *args)

    @property
    def signature(self):
        return Term(self.functor) / self.arity

    @property
    def arity(self):
        return len(self.args)

    def __call__(self, *args):
        return Term(self.functor, *args)

    def __eq__(self, other):
        if self is not other:
            return (self.functor == other.functor) and (self.args == other.args)
        else:
            return True

    def __hash__(self):
        tup = (self.functor,) + self.args
        return hash(tuple(map(hash, tup)))

    def __str__(self):
        return self.to_string(as_atom_flag=True)

    def to_string(self, as_atom_flag):
        return term_to_string(self, as_atom_flag)

    def __repr__(self):
        return str(self)

    def __truediv__(self, other):
        return Term('/', self, other)


class RoleTerm(Term):
    def __init__(self, term, role):
        if not isinstance(term, Term):
            raise TypeError
        super().__init__(term.functor, *term.args)
        self.role = role
    
    def strip_role(self):
        return Term(self.functor, *(self.args))
    
    def __str__(self):
        if isinstance(self.role, str):
            role_str = '"{}"'.format(str(self.role))
        else:
            role_str = str(self.role)
        return "{}@{}".format(super().__str__(), role_str)
    
    def __repr__(self):
        return str(self)


def symbols(names):
    if isinstance(names, str):
        names = names.replace(',', ' ')
        names = names.split()
    return map(Term, names)


class Clause(object):
    def __init__(self, head, body, mf_id):
        assert isinstance(mf_id, str) # XXX uncomment
        # assert mf_id is None or isinstance(mf_id, str) # XXX  remove
        self.head = head
        self.body = tuple(body)
        self.mf_id = mf_id
    
    def strip_roles(self):
        clause = Clause(
            head = self.head.strip_role(),
            body = [b.strip_role() for b in self.body],
            mf_id = self.mf_id
        )
        return clause

    def __str__(self):
        if self.body:
            return "{} :- {}.".format(self.head.to_string(True), ", ".join(map(lambda a:a.to_string(True), self.body)))
        else:
            return "{}.".format(str(self.head.to_string(True)))

