__author__ = 'ray'
from parser import Parser
from ListLexer import ListLexer
class ListParser(Parser):
    def __init__(self, input_lexer):
        Parser.__init__(self, input_lexer)
    #resolve stmt
    def stat(self):
        #attempt alternative 1: list EOF
        if self.speculate_stat_alt1():
            self.list()
            self.match(ListLexer.const_eof_type)
        elif self.speculate_stat_alt2():
            self.assign()
            self.match(ListLexer.const_eof_type)
        else:
            raise Exception("could not be resolved expceting stat found" + self.LT(1).to_string())
    def speculate_stat_alt1(self):
        success = True
        self.mark()
        try:
            self.list()
            self.match(ListLexer.const_eof_type)
        except Exception as err:
            success = False
            #print(err)
        self.release()
        return success
    def speculate_stat_alt2(self):
        success = True
        self.mark()
        try:
            self.assign()
            self.match(ListLexer.const_eof_type)
        except Exception as err:
            success = False
            #print(err)
        self.release()
        return success
    def assign(self):
        self.list()
        self.match(ListLexer.EQUALS)
        self.list()
    #resolve element
    def element(self):
        if self.LA(1) == ListLexer.NAME and self.LA(2) == ListLexer.EQUALS:
            self.match(ListLexer.NAME)
            self.match(ListLexer.EQUALS)
            self.match(ListLexer.NAME)
        elif self.LA(1) == ListLexer.NAME:
            self.match(ListLexer.NAME)
        elif self.LA(1) == ListLexer.LBRACK:
            self.list()
        else:
            raise Exception("expecting name or list: found" + self.LT(1).text)
    #resolve elements
    def elements(self):
        self.element()
        while self.LA(1) == ListLexer.COMMA:
            self.match(ListLexer.COMMA)
            self.element()
    #resolve list
    def list(self):
        self.match(ListLexer.LBRACK)
        self.elements()
        self.match(ListLexer.RBRACK)


