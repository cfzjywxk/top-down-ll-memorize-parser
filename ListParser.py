__author__ = 'ray'
from parser import Parser
from ListLexer import ListLexer
class ListParser(Parser):
    def __init__(self, input_lexer):
        Parser.__init__(self, input_lexer)
    #resolve element
    def element(self):
        if(self.look_ahead.type == ListLexer.NAME):
            self.match(ListLexer.NAME)
        elif(self.look_ahead.type == ListLexer.LBRACK):
            self.list()
        else:
            raise Exception("expectng name or list; found " + self.look_ahead.text)
    #resolve elements
    def elements(self):
        self.element()
        while(self.look_ahead.type == ListLexer.COMMA):
            self.match(ListLexer.COMMA)
            self.element()
    #resolve list
    def list(self):
        self.match(ListLexer.LBRACK)
        self.elements()
        self.match(ListLexer.RBRACK)


