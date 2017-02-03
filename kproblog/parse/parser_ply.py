from ply import lex
from ply import yacc
import re
from ..core import Term


class Lexer(object):
    tokens = (
        'STRING',
        'IDENT',
        'MIDENT',
        'NUM',
        'LP',
        'RP',
        'COMMA',
        'ADD',
        # 'AND',
        # 'BNOT',
        # 'LPAREN',
        # 'MOD',
        # 'MUL',
        # 'POW',
        # 'QUESTION',
        # 'RPAREN',
        # 'SLASH',
        # 'SUB',
        # 'XOR',
        # 'VBAR',
        # 'SUPREMUM',
        # 'INFIMUM'
    )

    # Tokens
    t_STRING = r'"((\\")|[^"])*"'
    t_IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_MIDENT = r'-[a-zA-Z_][a-zA-Z0-9_]*'
    t_NUM = r'-?[0-9]+'
    t_LP = r'\('
    t_RP = r'\)'
    t_COMMA = r','
    t_ADD = '\+'
    # t_AND      = '&'
    # t_BNOT     = '~'
    # t_LPAREN   = '('
    # t_MOD      = '\\'
    # t_MUL      = '*'
    # t_POW      = '**'
    # t_QUESTION = '?'
    # t_RPAREN   = ')'
    # t_SLASH    = '/'
    # t_SUB      = '-'
    # t_XOR      = '^'
    # t_VBAR     = '|'
    # t_SUPREMUM = '#sup'
    # t_INFIMUM  = '#inf'
    
    # t_SPACE = '[ \t]+'
    # t_ignore = '[ \t]+'

    def __init__(self, optimize):
        self.optimize = optimize
        self.lexer = lex.lex(object=self,optimize=optimize, lextab='asp_py_lextab')

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
    
    def t_error(self, t):
        print("Illegal character "+str(t.value[0]))
        t.lexer.skip(1)

class Parser(object):
    tokens = Lexer.tokens
    
    def __init__(self, lexer):
        self.lexer = lexer
        self.parser = yacc.yacc(module=self, tabmodule='asp_py_parsetab')

    def p_atom(self, t):
        """atom : IDENT LP terms RP
                | IDENT
                | MIDENT LP terms RP
                | MIDENT
        """
        if len(t) == 2:
            t[0] = Term(t[1])
        elif len(t) == 5:
            t[0] = Term(t[1], *t[3])
            

    def p_term(self, t):
        """term : term ADD term_nop
                | term_nop
        """
        t_len = len(t)
        if t_len == 2:
            t[0] = t[1]
        elif t_len == 4:
            t[0] = Term('+', t[1], t[3])
        else:
            raise SyntaxError

    def p_terms(self, t):
        """terms : term COMMA terms
                 | term
        """
        len_t = len(t)
        if len_t == 2:
            t[0] = [t[1]]
        elif len_t == 4:
            t[0] = [t[1]] + t[3]
        else:
            raise SyintaxError
    
    def p_term_nop(self, t):
        """term_nop  : IDENT LP terms RP
                     | STRING
                     | IDENT
                     | NUM
        """
        len_t = len(t)
        if len_t == 2:
            if isinstance(t[1], Term):
                t[0] = t[1]
            elif re.match(r'-?[0-9]+', t[1]) != None:
                t[0] = int(t[1])
            elif t[1][0] == '"' and t[1][-1] == '"':
                t[0] = str(t[1][1:-1])
            else:
                t[0] = Term(t[1])
        elif len_t == 5:
            _, functor, _, terms, _ = t
            t[0] = Term(functor, *terms)
        else:
            raise SyintaxError

    # | term AND term                     # And
    # | term ADD term                     # Add
    # | term SUB term                     # Sub

    def p_error(self, t):
        print("Syntax error at "+str(t))
        import inspect
        print (''.join(map(lambda x: "  %s:%s\n    %s" % (x[1], x[2], x[4][0]),inspect.stack())))

    def parse(self, line):
        line = line.strip()
        if len(line) > 0:
            return self.parser.parse(line, lexer=self.lexer.lexer)
        else:
            return None

lexer = Lexer(optimize=0)
parser = Parser(lexer)


def parse_term(term_str):
    return parser.parse(term_str)

