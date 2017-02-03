# Generated from parser/GringoGroundTerms.g4 by ANTLR 4.5.3
# encoding: utf-8
from antlr4 import *
from io import StringIO

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\26")
        buf.write("W\4\2\t\2\4\3\t\3\4\4\t\4\3\2\3\2\3\2\3\2\3\2\3\2\3\2")
        buf.write("\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3")
        buf.write("\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\5\2&\n\2\3\2\3\2\3")
        buf.write("\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2")
        buf.write("\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\7\2C\n\2")
        buf.write("\f\2\16\2F\13\2\3\3\3\3\3\3\3\3\3\3\3\3\7\3N\n\3\f\3\16")
        buf.write("\3Q\13\3\3\4\3\4\5\4U\n\4\3\4\2\4\2\4\5\2\4\6\2\2h\2%")
        buf.write("\3\2\2\2\4G\3\2\2\2\6T\3\2\2\2\b\t\b\2\1\2\t\n\7\13\2")
        buf.write("\2\n&\7\20\2\2\13\f\7\13\2\2\f\r\7\t\2\2\r&\7\20\2\2\16")
        buf.write("\17\7\13\2\2\17\20\5\4\3\2\20\21\7\20\2\2\21&\3\2\2\2")
        buf.write("\22\23\7\13\2\2\23\24\5\4\3\2\24\25\7\t\2\2\25\26\7\20")
        buf.write("\2\2\26&\3\2\2\2\27\30\7\4\2\2\30\31\7\13\2\2\31\32\5")
        buf.write("\6\4\2\32\33\7\20\2\2\33&\3\2\2\2\34\35\7\24\2\2\35\36")
        buf.write("\5\2\2\2\36\37\7\24\2\2\37&\3\2\2\2 &\7\4\2\2!&\7\3\2")
        buf.write("\2\"&\7\5\2\2#&\7\26\2\2$&\7\25\2\2%\b\3\2\2\2%\13\3\2")
        buf.write("\2\2%\16\3\2\2\2%\22\3\2\2\2%\27\3\2\2\2%\34\3\2\2\2%")
        buf.write(" \3\2\2\2%!\3\2\2\2%\"\3\2\2\2%#\3\2\2\2%$\3\2\2\2&D\3")
        buf.write("\2\2\2\'(\f\26\2\2()\7\23\2\2)C\5\2\2\27*+\f\25\2\2+,")
        buf.write("\7\17\2\2,C\5\2\2\26-.\f\24\2\2./\7\7\2\2/C\5\2\2\25\60")
        buf.write("\61\f\23\2\2\61\62\7\6\2\2\62C\5\2\2\24\63\64\f\22\2\2")
        buf.write("\64\65\7\22\2\2\65C\5\2\2\23\66\67\f\21\2\2\678\7\r\2")
        buf.write("\28C\5\2\2\229:\f\20\2\2:;\7\21\2\2;C\5\2\2\21<=\f\17")
        buf.write("\2\2=>\7\f\2\2>C\5\2\2\20?@\f\16\2\2@A\7\16\2\2AC\5\2")
        buf.write("\2\17B\'\3\2\2\2B*\3\2\2\2B-\3\2\2\2B\60\3\2\2\2B\63\3")
        buf.write("\2\2\2B\66\3\2\2\2B9\3\2\2\2B<\3\2\2\2B?\3\2\2\2CF\3\2")
        buf.write("\2\2DB\3\2\2\2DE\3\2\2\2E\3\3\2\2\2FD\3\2\2\2GH\b\3\1")
        buf.write("\2HI\5\2\2\2IO\3\2\2\2JK\f\3\2\2KL\7\t\2\2LN\5\2\2\2M")
        buf.write("J\3\2\2\2NQ\3\2\2\2OM\3\2\2\2OP\3\2\2\2P\5\3\2\2\2QO\3")
        buf.write("\2\2\2RU\5\4\3\2SU\3\2\2\2TR\3\2\2\2TS\3\2\2\2U\7\3\2")
        buf.write("\2\2\7%BDOT")
        return buf.getvalue()


class GringoGroundTermsParser ( Parser ):

    grammarFileName = "GringoGroundTerms.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'+'", "'&'", "'~'", "','", "<INVALID>", "'('", "'\\'", 
                     "'*'", "'**'", "'?'", "')'", "'/'", "'-'", "'^'", "'|'", 
                     "'#sup'", "'#inf'" ]

    symbolicNames = [ "<INVALID>", "NUMBER", "IDENTIFIER", "STRING", "ADD", 
                      "AND", "BNOT", "COMMA", "END", "LPAREN", "MOD", "MUL", 
                      "POW", "QUESTION", "RPAREN", "SLASH", "SUB", "XOR", 
                      "VBAR", "SUPREMUM", "INFIMUM" ]

    RULE_term = 0
    RULE_nterms = 1
    RULE_terms = 2

    ruleNames =  [ "term", "nterms", "terms" ]

    EOF = Token.EOF
    NUMBER=1
    IDENTIFIER=2
    STRING=3
    ADD=4
    AND=5
    BNOT=6
    COMMA=7
    END=8
    LPAREN=9
    MOD=10
    MUL=11
    POW=12
    QUESTION=13
    RPAREN=14
    SLASH=15
    SUB=16
    XOR=17
    VBAR=18
    SUPREMUM=19
    INFIMUM=20

    def __init__(self, input:TokenStream):
        super().__init__(input)
        self.checkVersion("4.5.3")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class TermContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return GringoGroundTermsParser.RULE_term

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class AddContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GringoGroundTermsParser.TermContext)
            else:
                return self.getTypedRuleContext(GringoGroundTermsParser.TermContext,i)

        def ADD(self):
            return self.getToken(GringoGroundTermsParser.ADD, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdd" ):
                listener.enterAdd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdd" ):
                listener.exitAdd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdd" ):
                return visitor.visitAdd(self)
            else:
                return visitor.visitChildren(self)


    class SubContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GringoGroundTermsParser.TermContext)
            else:
                return self.getTypedRuleContext(GringoGroundTermsParser.TermContext,i)

        def SUB(self):
            return self.getToken(GringoGroundTermsParser.SUB, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSub" ):
                listener.enterSub(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSub" ):
                listener.exitSub(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSub" ):
                return visitor.visitSub(self)
            else:
                return visitor.visitChildren(self)


    class ModContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GringoGroundTermsParser.TermContext)
            else:
                return self.getTypedRuleContext(GringoGroundTermsParser.TermContext,i)

        def MOD(self):
            return self.getToken(GringoGroundTermsParser.MOD, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMod" ):
                listener.enterMod(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMod" ):
                listener.exitMod(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMod" ):
                return visitor.visitMod(self)
            else:
                return visitor.visitChildren(self)


    class MulContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GringoGroundTermsParser.TermContext)
            else:
                return self.getTypedRuleContext(GringoGroundTermsParser.TermContext,i)

        def MUL(self):
            return self.getToken(GringoGroundTermsParser.MUL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMul" ):
                listener.enterMul(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMul" ):
                listener.exitMul(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMul" ):
                return visitor.visitMul(self)
            else:
                return visitor.visitChildren(self)


    class LparenCommaRparenContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(GringoGroundTermsParser.LPAREN, 0)
        def COMMA(self):
            return self.getToken(GringoGroundTermsParser.COMMA, 0)
        def RPAREN(self):
            return self.getToken(GringoGroundTermsParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLparenCommaRparen" ):
                listener.enterLparenCommaRparen(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLparenCommaRparen" ):
                listener.exitLparenCommaRparen(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLparenCommaRparen" ):
                return visitor.visitLparenCommaRparen(self)
            else:
                return visitor.visitChildren(self)


    class StringContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(GringoGroundTermsParser.STRING, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterString" ):
                listener.enterString(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitString" ):
                listener.exitString(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString" ):
                return visitor.visitString(self)
            else:
                return visitor.visitChildren(self)


    class SupremumContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def SUPREMUM(self):
            return self.getToken(GringoGroundTermsParser.SUPREMUM, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSupremum" ):
                listener.enterSupremum(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSupremum" ):
                listener.exitSupremum(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSupremum" ):
                return visitor.visitSupremum(self)
            else:
                return visitor.visitChildren(self)


    class IdentifierContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IDENTIFIER(self):
            return self.getToken(GringoGroundTermsParser.IDENTIFIER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentifier" ):
                listener.enterIdentifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentifier" ):
                listener.exitIdentifier(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdentifier" ):
                return visitor.visitIdentifier(self)
            else:
                return visitor.visitChildren(self)


    class LparenRparenContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(GringoGroundTermsParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(GringoGroundTermsParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLparenRparen" ):
                listener.enterLparenRparen(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLparenRparen" ):
                listener.exitLparenRparen(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLparenRparen" ):
                return visitor.visitLparenRparen(self)
            else:
                return visitor.visitChildren(self)


    class NumberContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUMBER(self):
            return self.getToken(GringoGroundTermsParser.NUMBER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumber" ):
                return visitor.visitNumber(self)
            else:
                return visitor.visitChildren(self)


    class IdentifierLparenTermsRparenContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IDENTIFIER(self):
            return self.getToken(GringoGroundTermsParser.IDENTIFIER, 0)
        def LPAREN(self):
            return self.getToken(GringoGroundTermsParser.LPAREN, 0)
        def terms(self):
            return self.getTypedRuleContext(GringoGroundTermsParser.TermsContext,0)

        def RPAREN(self):
            return self.getToken(GringoGroundTermsParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentifierLparenTermsRparen" ):
                listener.enterIdentifierLparenTermsRparen(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentifierLparenTermsRparen" ):
                listener.exitIdentifierLparenTermsRparen(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdentifierLparenTermsRparen" ):
                return visitor.visitIdentifierLparenTermsRparen(self)
            else:
                return visitor.visitChildren(self)


    class VbarTermVbarContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def VBAR(self, i:int=None):
            if i is None:
                return self.getTokens(GringoGroundTermsParser.VBAR)
            else:
                return self.getToken(GringoGroundTermsParser.VBAR, i)
        def term(self):
            return self.getTypedRuleContext(GringoGroundTermsParser.TermContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVbarTermVbar" ):
                listener.enterVbarTermVbar(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVbarTermVbar" ):
                listener.exitVbarTermVbar(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVbarTermVbar" ):
                return visitor.visitVbarTermVbar(self)
            else:
                return visitor.visitChildren(self)


    class AndContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GringoGroundTermsParser.TermContext)
            else:
                return self.getTypedRuleContext(GringoGroundTermsParser.TermContext,i)

        def AND(self):
            return self.getToken(GringoGroundTermsParser.AND, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnd" ):
                listener.enterAnd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnd" ):
                listener.exitAnd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnd" ):
                return visitor.visitAnd(self)
            else:
                return visitor.visitChildren(self)


    class LparenNTermsRparenContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(GringoGroundTermsParser.LPAREN, 0)
        def nterms(self):
            return self.getTypedRuleContext(GringoGroundTermsParser.NtermsContext,0)

        def RPAREN(self):
            return self.getToken(GringoGroundTermsParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLparenNTermsRparen" ):
                listener.enterLparenNTermsRparen(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLparenNTermsRparen" ):
                listener.exitLparenNTermsRparen(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLparenNTermsRparen" ):
                return visitor.visitLparenNTermsRparen(self)
            else:
                return visitor.visitChildren(self)


    class InfimumContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INFIMUM(self):
            return self.getToken(GringoGroundTermsParser.INFIMUM, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInfimum" ):
                listener.enterInfimum(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInfimum" ):
                listener.exitInfimum(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInfimum" ):
                return visitor.visitInfimum(self)
            else:
                return visitor.visitChildren(self)


    class SlashContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GringoGroundTermsParser.TermContext)
            else:
                return self.getTypedRuleContext(GringoGroundTermsParser.TermContext,i)

        def SLASH(self):
            return self.getToken(GringoGroundTermsParser.SLASH, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSlash" ):
                listener.enterSlash(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSlash" ):
                listener.exitSlash(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSlash" ):
                return visitor.visitSlash(self)
            else:
                return visitor.visitChildren(self)


    class PowContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GringoGroundTermsParser.TermContext)
            else:
                return self.getTypedRuleContext(GringoGroundTermsParser.TermContext,i)

        def POW(self):
            return self.getToken(GringoGroundTermsParser.POW, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPow" ):
                listener.enterPow(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPow" ):
                listener.exitPow(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPow" ):
                return visitor.visitPow(self)
            else:
                return visitor.visitChildren(self)


    class XorContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GringoGroundTermsParser.TermContext)
            else:
                return self.getTypedRuleContext(GringoGroundTermsParser.TermContext,i)

        def XOR(self):
            return self.getToken(GringoGroundTermsParser.XOR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterXor" ):
                listener.enterXor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitXor" ):
                listener.exitXor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitXor" ):
                return visitor.visitXor(self)
            else:
                return visitor.visitChildren(self)


    class QuestionContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GringoGroundTermsParser.TermContext)
            else:
                return self.getTypedRuleContext(GringoGroundTermsParser.TermContext,i)

        def QUESTION(self):
            return self.getToken(GringoGroundTermsParser.QUESTION, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuestion" ):
                listener.enterQuestion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuestion" ):
                listener.exitQuestion(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuestion" ):
                return visitor.visitQuestion(self)
            else:
                return visitor.visitChildren(self)


    class LparenNTermsCommaRparenContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(GringoGroundTermsParser.LPAREN, 0)
        def nterms(self):
            return self.getTypedRuleContext(GringoGroundTermsParser.NtermsContext,0)

        def COMMA(self):
            return self.getToken(GringoGroundTermsParser.COMMA, 0)
        def RPAREN(self):
            return self.getToken(GringoGroundTermsParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLparenNTermsCommaRparen" ):
                listener.enterLparenNTermsCommaRparen(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLparenNTermsCommaRparen" ):
                listener.exitLparenNTermsCommaRparen(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLparenNTermsCommaRparen" ):
                return visitor.visitLparenNTermsCommaRparen(self)
            else:
                return visitor.visitChildren(self)



    def term(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = GringoGroundTermsParser.TermContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 0
        self.enterRecursionRule(localctx, 0, self.RULE_term, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self._errHandler.sync(self);
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                localctx = GringoGroundTermsParser.LparenRparenContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 7
                self.match(GringoGroundTermsParser.LPAREN)
                self.state = 8
                self.match(GringoGroundTermsParser.RPAREN)
                pass

            elif la_ == 2:
                localctx = GringoGroundTermsParser.LparenCommaRparenContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 9
                self.match(GringoGroundTermsParser.LPAREN)
                self.state = 10
                self.match(GringoGroundTermsParser.COMMA)
                self.state = 11
                self.match(GringoGroundTermsParser.RPAREN)
                pass

            elif la_ == 3:
                localctx = GringoGroundTermsParser.LparenNTermsRparenContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 12
                self.match(GringoGroundTermsParser.LPAREN)
                self.state = 13
                self.nterms(0)
                self.state = 14
                self.match(GringoGroundTermsParser.RPAREN)
                pass

            elif la_ == 4:
                localctx = GringoGroundTermsParser.LparenNTermsCommaRparenContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 16
                self.match(GringoGroundTermsParser.LPAREN)
                self.state = 17
                self.nterms(0)
                self.state = 18
                self.match(GringoGroundTermsParser.COMMA)
                self.state = 19
                self.match(GringoGroundTermsParser.RPAREN)
                pass

            elif la_ == 5:
                localctx = GringoGroundTermsParser.IdentifierLparenTermsRparenContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 21
                self.match(GringoGroundTermsParser.IDENTIFIER)
                self.state = 22
                self.match(GringoGroundTermsParser.LPAREN)
                self.state = 23
                self.terms()
                self.state = 24
                self.match(GringoGroundTermsParser.RPAREN)
                pass

            elif la_ == 6:
                localctx = GringoGroundTermsParser.VbarTermVbarContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 26
                self.match(GringoGroundTermsParser.VBAR)
                self.state = 27
                self.term(0)
                self.state = 28
                self.match(GringoGroundTermsParser.VBAR)
                pass

            elif la_ == 7:
                localctx = GringoGroundTermsParser.IdentifierContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 30
                self.match(GringoGroundTermsParser.IDENTIFIER)
                pass

            elif la_ == 8:
                localctx = GringoGroundTermsParser.NumberContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 31
                self.match(GringoGroundTermsParser.NUMBER)
                pass

            elif la_ == 9:
                localctx = GringoGroundTermsParser.StringContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 32
                self.match(GringoGroundTermsParser.STRING)
                pass

            elif la_ == 10:
                localctx = GringoGroundTermsParser.InfimumContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 33
                self.match(GringoGroundTermsParser.INFIMUM)
                pass

            elif la_ == 11:
                localctx = GringoGroundTermsParser.SupremumContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 34
                self.match(GringoGroundTermsParser.SUPREMUM)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 66
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 64
                    self._errHandler.sync(self);
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = GringoGroundTermsParser.XorContext(self, GringoGroundTermsParser.TermContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_term)
                        self.state = 37
                        if not self.precpred(self._ctx, 20):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 20)")
                        self.state = 38
                        self.match(GringoGroundTermsParser.XOR)
                        self.state = 39
                        self.term(21)
                        pass

                    elif la_ == 2:
                        localctx = GringoGroundTermsParser.QuestionContext(self, GringoGroundTermsParser.TermContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_term)
                        self.state = 40
                        if not self.precpred(self._ctx, 19):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 19)")
                        self.state = 41
                        self.match(GringoGroundTermsParser.QUESTION)
                        self.state = 42
                        self.term(20)
                        pass

                    elif la_ == 3:
                        localctx = GringoGroundTermsParser.AndContext(self, GringoGroundTermsParser.TermContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_term)
                        self.state = 43
                        if not self.precpred(self._ctx, 18):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 18)")
                        self.state = 44
                        self.match(GringoGroundTermsParser.AND)
                        self.state = 45
                        self.term(19)
                        pass

                    elif la_ == 4:
                        localctx = GringoGroundTermsParser.AddContext(self, GringoGroundTermsParser.TermContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_term)
                        self.state = 46
                        if not self.precpred(self._ctx, 17):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 17)")
                        self.state = 47
                        self.match(GringoGroundTermsParser.ADD)
                        self.state = 48
                        self.term(18)
                        pass

                    elif la_ == 5:
                        localctx = GringoGroundTermsParser.SubContext(self, GringoGroundTermsParser.TermContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_term)
                        self.state = 49
                        if not self.precpred(self._ctx, 16):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 16)")
                        self.state = 50
                        self.match(GringoGroundTermsParser.SUB)
                        self.state = 51
                        self.term(17)
                        pass

                    elif la_ == 6:
                        localctx = GringoGroundTermsParser.MulContext(self, GringoGroundTermsParser.TermContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_term)
                        self.state = 52
                        if not self.precpred(self._ctx, 15):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 15)")
                        self.state = 53
                        self.match(GringoGroundTermsParser.MUL)
                        self.state = 54
                        self.term(16)
                        pass

                    elif la_ == 7:
                        localctx = GringoGroundTermsParser.SlashContext(self, GringoGroundTermsParser.TermContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_term)
                        self.state = 55
                        if not self.precpred(self._ctx, 14):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 14)")
                        self.state = 56
                        self.match(GringoGroundTermsParser.SLASH)
                        self.state = 57
                        self.term(15)
                        pass

                    elif la_ == 8:
                        localctx = GringoGroundTermsParser.ModContext(self, GringoGroundTermsParser.TermContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_term)
                        self.state = 58
                        if not self.precpred(self._ctx, 13):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 13)")
                        self.state = 59
                        self.match(GringoGroundTermsParser.MOD)
                        self.state = 60
                        self.term(14)
                        pass

                    elif la_ == 9:
                        localctx = GringoGroundTermsParser.PowContext(self, GringoGroundTermsParser.TermContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_term)
                        self.state = 61
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 62
                        self.match(GringoGroundTermsParser.POW)
                        self.state = 63
                        self.term(13)
                        pass

             
                self.state = 68
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class NtermsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return GringoGroundTermsParser.RULE_nterms

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class ManyTermsContext(NtermsContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.NtermsContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def nterms(self):
            return self.getTypedRuleContext(GringoGroundTermsParser.NtermsContext,0)

        def COMMA(self):
            return self.getToken(GringoGroundTermsParser.COMMA, 0)
        def term(self):
            return self.getTypedRuleContext(GringoGroundTermsParser.TermContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterManyTerms" ):
                listener.enterManyTerms(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitManyTerms" ):
                listener.exitManyTerms(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitManyTerms" ):
                return visitor.visitManyTerms(self)
            else:
                return visitor.visitChildren(self)


    class OneTermContext(NtermsContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GringoGroundTermsParser.NtermsContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def term(self):
            return self.getTypedRuleContext(GringoGroundTermsParser.TermContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOneTerm" ):
                listener.enterOneTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOneTerm" ):
                listener.exitOneTerm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOneTerm" ):
                return visitor.visitOneTerm(self)
            else:
                return visitor.visitChildren(self)



    def nterms(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = GringoGroundTermsParser.NtermsContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_nterms, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            localctx = GringoGroundTermsParser.OneTermContext(self, localctx)
            self._ctx = localctx
            _prevctx = localctx

            self.state = 70
            self.term(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 77
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = GringoGroundTermsParser.ManyTermsContext(self, GringoGroundTermsParser.NtermsContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_nterms)
                    self.state = 72
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 73
                    self.match(GringoGroundTermsParser.COMMA)
                    self.state = 74
                    self.term(0) 
                self.state = 79
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class TermsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def nterms(self):
            return self.getTypedRuleContext(GringoGroundTermsParser.NtermsContext,0)


        def getRuleIndex(self):
            return GringoGroundTermsParser.RULE_terms

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerms" ):
                listener.enterTerms(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerms" ):
                listener.exitTerms(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerms" ):
                return visitor.visitTerms(self)
            else:
                return visitor.visitChildren(self)




    def terms(self):

        localctx = GringoGroundTermsParser.TermsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_terms)
        try:
            self.state = 82
            token = self._input.LA(1)
            if token in [GringoGroundTermsParser.NUMBER, GringoGroundTermsParser.IDENTIFIER, GringoGroundTermsParser.STRING, GringoGroundTermsParser.LPAREN, GringoGroundTermsParser.VBAR, GringoGroundTermsParser.SUPREMUM, GringoGroundTermsParser.INFIMUM]:
                self.enterOuterAlt(localctx, 1)
                self.state = 80
                self.nterms(0)

            elif token in [GringoGroundTermsParser.RPAREN]:
                self.enterOuterAlt(localctx, 2)


            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[0] = self.term_sempred
        self._predicates[1] = self.nterms_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def term_sempred(self, localctx:TermContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 20)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 19)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 18)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 17)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 16)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 15)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 14)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 13)
         

            if predIndex == 8:
                return self.precpred(self._ctx, 12)
         

    def nterms_sempred(self, localctx:NtermsContext, predIndex:int):
            if predIndex == 9:
                return self.precpred(self._ctx, 1)
         




