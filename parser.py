__author__ = 'ray'
from ListLexer import ListLexer
class Parser(object):
    Failed = 1
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
            self.clear_memo()
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
    def already_parsed_rule(self, memo):
        memo_index = memo.get(self.get_index())
        if memo_index is None:
            return False
        print("parsed list before at index " + str(self.get_index()) + "; skip ahead to token index "
                + str(memo_index) + ":" + self.look_ahead[memo_index].text)
        if memo_index == Parser.Failed:
            raise Exception("previous parse failed!") #to stop further parsing
        self.seek(memo_index)
        return True
    def get_index(self):
        return self.p
    def clear_memo(self):
        pass
    def memorize(self, memo, start_index, is_succ):
        stop_index = None
        if is_succ == Parser.Failed:
            stop_index = Parser.Failed
        else:
            stop_index = self.get_index()
        memo[start_index] = stop_index
if __name__ == '__main__':
    print("this is the Parse class def")
    test_str = '[a,b,a,c]=ad'
    list_lexer = ListLexer(test_str)

