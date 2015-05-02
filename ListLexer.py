__author__ = 'ray'
from lexer import lexer

class Token:
    type = 0
    text = ''
    def __init__(self, type, text):
        self.type = type
        self.text = text
    def to_string(self):
        print(self.type)
        str_name = ListLexer.TokenNames[self.type]
        return "<'" + str_name + "'," + str_name + ">"

class ListLexer(lexer):
    NAME = 2
    COMMA = 3
    LBRACK = 4
    RBRACK = 5
    TokenNames = [ "n/a", "<EOF>", "NAME", "COMMA", "LBRACK", "RBRACK"]
    def get_token_name(self, token_type):
        return ListLexer.TokenNames[token_type]
    def __init__(self, input_str):
        lexer.__init__(self, input_str)
    def next_token(self):
        while self.cur_char != ListLexer.const_eof:
            if self.cur_char in [' ', '\n', '\r', '\t']:
                self.ws()
                continue
            elif self.cur_char == ',':
                self.consume()
                return Token(ListLexer.COMMA, ',')
            elif self.cur_char == '[':
                self.consume()
                return Token(ListLexer.LBRACK, '[')
            elif self.cur_char == ']':
                self.consume()
                return Token(ListLexer.RBRACK, ']')
            else:
                if self.cur_char.isalpha():
                    return self.get_name()
                else:
                    raise Exception("invalid character: " + self.cur_char)
    def get_name(self):
        tmp_str = ""
        tmp_str += self.cur_char
        self.LETTER()
        while(self.isLETTER()):
            tmp_str += self.cur_char
            self.LETTER()
        return Token(ListLexer.NAME, tmp_str)

    def LETTER(self):
        if self.isLETTER():
            self.consume()
        else:
            raise Exception("expecting LETTER; found" + self.cur_char)

    def isLETTER(self):
        return self.cur_char.isalpha()

    def ws(self):
        while(self.cur_char in [" \n\t\r"]):
            self.consume()

if __name__ == '__main__':
    print("this is the listLexer class def")
    test_str = '[a,b,a,c]'
    list_lexer = ListLexer(test_str)
    while list_lexer.cur_char != ListLexer.const_eof:
        print("current curchar is : " + list_lexer.cur_char)
        t = list_lexer.next_token()
        print(t.to_string())
