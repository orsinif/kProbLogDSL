# Generated from parser/GringoGroundTerms.g4 by ANTLR 4.5.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GringoGroundTermsParser import GringoGroundTermsParser
else:
    from GringoGroundTermsParser import GringoGroundTermsParser

# This class defines a complete generic visitor for a parse tree produced by GringoGroundTermsParser.

class GringoGroundTermsVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by GringoGroundTermsParser#Add.
    def visitAdd(self, ctx:GringoGroundTermsParser.AddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#Sub.
    def visitSub(self, ctx:GringoGroundTermsParser.SubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#Mod.
    def visitMod(self, ctx:GringoGroundTermsParser.ModContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#Mul.
    def visitMul(self, ctx:GringoGroundTermsParser.MulContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#LparenCommaRparen.
    def visitLparenCommaRparen(self, ctx:GringoGroundTermsParser.LparenCommaRparenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#String.
    def visitString(self, ctx:GringoGroundTermsParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#Supremum.
    def visitSupremum(self, ctx:GringoGroundTermsParser.SupremumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#Identifier.
    def visitIdentifier(self, ctx:GringoGroundTermsParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#LparenRparen.
    def visitLparenRparen(self, ctx:GringoGroundTermsParser.LparenRparenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#Number.
    def visitNumber(self, ctx:GringoGroundTermsParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#IdentifierLparenTermsRparen.
    def visitIdentifierLparenTermsRparen(self, ctx:GringoGroundTermsParser.IdentifierLparenTermsRparenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#VbarTermVbar.
    def visitVbarTermVbar(self, ctx:GringoGroundTermsParser.VbarTermVbarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#And.
    def visitAnd(self, ctx:GringoGroundTermsParser.AndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#LparenNTermsRparen.
    def visitLparenNTermsRparen(self, ctx:GringoGroundTermsParser.LparenNTermsRparenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#Infimum.
    def visitInfimum(self, ctx:GringoGroundTermsParser.InfimumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#Slash.
    def visitSlash(self, ctx:GringoGroundTermsParser.SlashContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#Pow.
    def visitPow(self, ctx:GringoGroundTermsParser.PowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#Xor.
    def visitXor(self, ctx:GringoGroundTermsParser.XorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#Question.
    def visitQuestion(self, ctx:GringoGroundTermsParser.QuestionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#LparenNTermsCommaRparen.
    def visitLparenNTermsCommaRparen(self, ctx:GringoGroundTermsParser.LparenNTermsCommaRparenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#ManyTerms.
    def visitManyTerms(self, ctx:GringoGroundTermsParser.ManyTermsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#OneTerm.
    def visitOneTerm(self, ctx:GringoGroundTermsParser.OneTermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GringoGroundTermsParser#terms.
    def visitTerms(self, ctx:GringoGroundTermsParser.TermsContext):
        return self.visitChildren(ctx)



del GringoGroundTermsParser