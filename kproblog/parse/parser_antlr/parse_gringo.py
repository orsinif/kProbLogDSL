from antlr4 import *

from .GringoGroundTermsLexer import GringoGroundTermsLexer
from .GringoGroundTermsParser import GringoGroundTermsParser
from .GringoGroundTermsVisitor import GringoGroundTermsVisitor as BaseGringoGroundTermsVisitor

from ...core import Term, Clause, symbols
from ...utils import TimeContext

def parse_term(term_str):
    # print("term_str", term_str)
    input_stram = InputStream(term_str)
    # with TimeContext("GringoGroundTermsLexer"):
    lexer = GringoGroundTermsLexer(input_stram)
    stream = CommonTokenStream(lexer)
    # with TimeContext("GringoGroundTermsParser"):
    parser = GringoGroundTermsParser(stream)
    tree = parser.term()
    # with TimeContext("GringoGroundTermsVisitor"):
    visitor = GringoGroundTermsVisitor()
    return visitor.visit(tree)

# def parse_clause(clause_str):
#     clause_str = clause_str.strip()
#     if not clause_str.islower():
#         raise ValueError('clause "{}" is not ground'.format(clause_str))
#     clause_str = "".join(clause_str.split()) # WE ARE SPACE INSENSITIVE
#     assert clause_str[-1] == '.'
#     clause_str = clause_str[:-1]
#     clause_str_list = clause_str.split(':-')
#
#     head, *_ = map(parse_term, clause_str_list)
#
#     assert head.functor == 'is_true'
#     mf_id, true_head, true_body = head.args
#
#     query_flag = mf_id.functor == 'query'
#
#
#     if true_body.functor == 'true':
#         return query_flag, Clause(true_head, (), mf_id.functor)
#     elif true_body.functor == 'conj':
#         return query_flag, Clause(true_head, true_body.args, mf_id.functor)
#     else:
#         raise Error
    
    


class GringoGroundTermsVisitor(BaseGringoGroundTermsVisitor):
    
    def helperVisitBinaryOperation(self, ctx, op):
        assert len(ctx.children) == 3
        term_a = self.visit(ctx.children[0]); assert isinstance(term_a, Term) or isinstance(term_a, int) or isinstance(term_b, str)
        assert ctx.children[1].getText() == op
        term_b = self.visit(ctx.children[2]); assert isinstance(term_b, Term) or isinstance(term_b, int) or isinstance(term_b, str)
        return Term(op, term_a, term_b)
        
        
    # Visit a parse tree produced by GringoGroundTermsParser#Add.
    def visitAdd(self, ctx:GringoGroundTermsParser.AddContext):
        return self.helperVisitBinaryOperation(ctx, op='+')


    # Visit a parse tree produced by GringoGroundTermsParser#Sub.
    def visitSub(self, ctx:GringoGroundTermsParser.SubContext):
        return self.helperVisitBinaryOperation(ctx, op='-')


    # Visit a parse tree produced by GringoGroundTermsParser#Mod.
    def visitMod(self, ctx:GringoGroundTermsParser.ModContext):
        raise NotImplementedError
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#Mul.
    def visitMul(self, ctx:GringoGroundTermsParser.MulContext):
        return self.helperVisitBinaryOperation(ctx, op='*')


    # Visit a parse tree produced by GringoGroundTermsParser#LparenCommaRparen.
    def visitLparenCommaRparen(self, ctx:GringoGroundTermsParser.LparenCommaRparenContext):
        raise NotImplementedError
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#String.
    def visitString(self, ctx:GringoGroundTermsParser.StringContext):
        s = ctx.getText()
        assert s[0] == '"' and s[-1] == '"'
        return s[1:-1]


    # Visit a parse tree produced by GringoGroundTermsParser#Supremum.
    def visitSupremum(self, ctx:GringoGroundTermsParser.SupremumContext):
        raise NotImplementedError
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#Identifier.
    def visitIdentifier(self, ctx:GringoGroundTermsParser.IdentifierContext):
        functor = str(ctx.IDENTIFIER().getText())
        return Term(functor)

    # Visit a parse tree produced by GringoGroundTermsParser#LparenRparen.
    def visitLparenRparen(self, ctx:GringoGroundTermsParser.LparenRparenContext):
        raise NotImplementedError
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#Number.
    def visitNumber(self, ctx:GringoGroundTermsParser.NumberContext):
        return int(ctx.getText())


    # Visit a parse tree produced by GringoGroundTermsParser#IdentifierLparenTermsRparen.
    def visitIdentifierLparenTermsRparen(self, ctx:GringoGroundTermsParser.IdentifierLparenTermsRparenContext):
        functor = str(ctx.IDENTIFIER().getText())
        if ctx.terms().children is not None:
            # print(">>", ctx.terms().children, end='')
            # print([ch.getText() for ch in ctx.terms().children])
            args = self.visitChildren(ctx.terms())
            return Term(functor, *args)
        else:
            return Term(functor)
            
        
    # Visit a parse tree produced by GringoGroundTermsParser#VbarTermVbar.
    def visitVbarTermVbar(self, ctx:GringoGroundTermsParser.VbarTermVbarContext):
        raise NotImplementedError
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#And.
    def visitAnd(self, ctx:GringoGroundTermsParser.AndContext):
        return self.helperVisitBinaryOperation(ctx, op='&')

    # Visit a parse tree produced by GringoGroundTermsParser#LparenNTermsRparen.
    def visitLparenNTermsRparen(self, ctx:GringoGroundTermsParser.LparenNTermsRparenContext):
        raise NotImplementedError
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#Infimum.
    def visitInfimum(self, ctx:GringoGroundTermsParser.InfimumContext):
        raise NotImplementedError
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#Slash.
    def visitSlash(self, ctx:GringoGroundTermsParser.SlashContext):
        return self.helperVisitBinaryOperation(ctx, op='/')


    # Visit a parse tree produced by GringoGroundTermsParser#Pow.
    def visitPow(self, ctx:GringoGroundTermsParser.PowContext):
        return self.helperVisitBinaryOperation(ctx, op='**')

    # Visit a parse tree produced by GringoGroundTermsParser#Xor.
    def visitXor(self, ctx:GringoGroundTermsParser.XorContext):
        return self.helperVisitBinaryOperation(ctx, op='^')


    # Visit a parse tree produced by GringoGroundTermsParser#Question.
    def visitQuestion(self, ctx:GringoGroundTermsParser.QuestionContext):
        return self.helperVisitBinaryOperation(ctx, op='?')


    # Visit a parse tree produced by GringoGroundTermsParser#LparenNTermsCommaRparen.
    def visitLparenNTermsCommaRparen(self, ctx:GringoGroundTermsParser.LparenNTermsCommaRparenContext):
        raise NotImplementedError
        return self.visitChildren(ctx)

    def visitManyTerms(self, ctx:GringoGroundTermsParser.ManyTermsContext):
        nterms = self.visit(ctx.getChild(0)) # TUPLE
        assert ctx.getChild(1).getText() == ','
        one_term = self.visit(ctx.getChild(2)) # ONE TERM IN A TUPLE
        return nterms + (one_term,) 


    def visitOneTerm(self, ctx:GringoGroundTermsParser.OneTermContext):
        term = self.visit(ctx.getChild(0))
        assert isinstance(term, Term) or isinstance(term, int), "type {}".format(str(type(term)))
        return (term, )

