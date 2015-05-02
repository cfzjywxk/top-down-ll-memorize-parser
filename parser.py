__author__ = 'ray'
from ListLexer import ListLexer
class Parser(object):
    def __init__(self, lexer_input):
        self.input = lexer_input
        self.p = 0
        self.look_ahead = []
        self.markers = []
        self.sync(1)
    def consume(self):
        self.p += 1
        if self.p == len(self.look_ahead) and (not self.isSpaculating()):
            self.p = 0
            self.look_ahead = []
        self.sync(1)
    def LT(self, i):
        self.sync(i)
        return self.look_ahead[self.p + i - 1]
    def LA(self, i):
        return self.LT(i).type
    def match(self, x):
        if self.LA(1) == x:
            self.consume()
        else:
            raise Exception("expcting " + self.input.get_token_name(x)\
                + ";found " + self.LT(1).text )
    def sync(self, i):
        if self.p + i - 1 > (len(self.look_ahead) - 1):
            n = self.p + i - 1 - (len(self.look_ahead) - 1)
            self.fill(n)
    def fill(self, n):
        for i in range(1, n + 1):
            self.look_ahead.append(self.input.next_token())
    def mark(self):
        self.markers.append(self.p)
        return self.p
    def release(self):
        marker = self.markers[len(self.markers) - 1]
        self.markers.remove(len(self.markers) - 1)
        self.seek(marker)
    def seek(self, index):
        self.p = index
    def isSpaculating(self):
        return len(self.markers) > 0

if __name__ == '__main__':
    print("this is the Parse class def")
    test_str = '[a,b,a,c]=ad'
    list_lexer = ListLexer(test_str)

