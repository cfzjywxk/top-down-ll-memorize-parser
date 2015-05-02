__author__ = 'ray'
from parser import Parser
from ListLexer import ListLexer
class ListParser(Parser):
    def __init__(self, input_lexer, k):
        Parser.__init__(self, input_lexer, k)
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


