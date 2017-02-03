from ..core import symbols, Clause, Term

from ..config import CLAUSE_PARSER

if CLAUSE_PARSER == 'tricky':
    from .parser_tricky import parse_term
elif CLAUSE_PARSER == 'antlr4':
    from .parser_antlr import parse_term
elif CLAUSE_PARSER == 'ply':
    from .parser_ply import parse_term
else:
    raise ValueError


def recover_infix(terms, inv_infix_dict):
    res = []
    for term in terms:
        if term.arity == 2 and term.functor in inv_infix_dict:
            # print('inv_infix_dict[term.functor]', inv_infix_dict[term.functor])
            term = Term(inv_infix_dict[term.functor], *term.args)
            # print("XXX:", term, "functor:", term.functor, 'args', term.args)
        res.append(term)
    return tuple(res)
    


def parse_clause(clause_str, inv_infix_dict):
    clause_str = clause_str.strip()
    if not clause_str.islower():
        raise ValueError('clause "{}" is not ground'.format(clause_str))
    clause_str = "".join(clause_str.split()) # WE ARE SPACE INSENSITIVE
    assert clause_str[-1] == '.'
    clause_str = clause_str[:-1]
    clause_str_list = clause_str.split(':-')

    head, *_ = map(parse_term, clause_str_list)
    assert head.functor == 'is_true'
    mf_id, true_head, true_body = head.args

    query_flag = mf_id.functor == 'query'


    if true_body.functor == 'true':
        return query_flag, Clause(true_head, (), mf_id.functor)
    elif true_body.functor == 'conj':
        return query_flag, Clause(true_head, recover_infix(true_body.args, inv_infix_dict), mf_id.functor)
    else:
        raise Error
