grammar GringoGroundTerms;

NUMBER
    : '0'
    | [1-9] [0-9]*
    ;

IDENTIFIER:'_'*[a-z]['A-Za-z0-9_]*;

STRING : '"'('\"'|['A-Za-z0-9_ ])*?'"';



/*STRING     = "\"" ([^\\"\n]|"\\\""|"\\\\"|"\\n")* "\"";*/




ADD      :   '+';
AND      :   '&';
BNOT     :   '~';
COMMA    :   ',';
END      :   '0' EOF;
LPAREN   :   '(';
MOD      :   '\\';
MUL      :   '*';
POW      :   '**';
QUESTION :   '?';
RPAREN   :   ')';
SLASH    :   '/';
SUB      :   '-';
XOR      :   '^';
VBAR     :   '|';
SUPREMUM :   '#sup';
INFIMUM  :   '#inf';

term
    : term XOR term                     # Xor 
    | term QUESTION term                # Question
    | term AND term                     # And
    | term ADD term                     # Add
    | term SUB term                     # Sub
    | term MUL term                     # Mul
    | term SLASH term                   # Slash
    | term MOD term                     # Mod
    | term POW term                     # Pow
/*  
    | SUB term %prec UMINUS
    | BNOT term %prec UBNOT             
*/  
    | LPAREN RPAREN                     # LparenRparen
    | LPAREN COMMA RPAREN               # LparenCommaRparen
    | LPAREN nterms RPAREN              # LparenNTermsRparen
    | LPAREN nterms COMMA RPAREN        # LparenNTermsCommaRparen 
    | IDENTIFIER LPAREN terms RPAREN    # IdentifierLparenTermsRparen
    | VBAR term VBAR                    # VbarTermVbar
    | IDENTIFIER                        # Identifier
    | NUMBER                            # Number
    | STRING                            # String
    | INFIMUM                           # Infimum
    | SUPREMUM                          # Supremum
    ;

nterms
    : term                              # OneTerm
    | nterms COMMA term                 # ManyTerms
    ;

terms
    : nterms
    |
    ;