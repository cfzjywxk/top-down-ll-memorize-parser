__author__ = 'ray'
from lexer import lexer
from ListLexer import ListLexer
class Parser(object):
    def __init__(self, lexer_input, num):
        self.input = lexer_input
        self.k = num
        self.p = 0
        self.look_ahead = []
        for i in range(1, self.k + 1):
            self.look_ahead.append(None)
        for i in range(1, self.k + 1):
            self.consume()
    def consume(self):
        self.look_ahead[self.p] = self.input.next_token()
        self.p = (self.p + 1) % self.k
    def LT(self, i):
        return self.look_ahead[(self.p + i - 1) % self.k]
    def LA(self, i):
        return self.LT(i).type
    def match(self, x):
        if self.LA(1) == x:
            self.consume()
        else:
            raise Exception("expcting " + self.input.get_token_name(x)\
                + ";found " + self.LT(1).text )


if __name__ == '__main__':
    print("this is the Parse class def")
    test_str = '[a,b,a,c]=ad'
    list_lexer = ListLexer(test_str)

