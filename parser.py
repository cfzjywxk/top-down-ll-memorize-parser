__author__ = 'ray'
from lexer import lexer

class Parser(object):
    def __init__(self, lexer_input):
        self.input = lexer_input
        self.consume()
    def consume(self):
        self.look_ahead = self.input.next_token()
    def match(self, x):
        if(self.look_ahead.type == x):
            self.consume()
        else:
            raise Exception("expecting " + self.input.get_token_name(x) +\
                " ; found " + self.look_ahead.text)

