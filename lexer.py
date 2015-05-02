class lexer(object):
    const_eof = ''
    const_eof_type = 1
    def __init__(self, input_str):
        self.input_str = input_str
        self.cur_index = 0
        self.cur_char = input_str[self.cur_index]
    def consume(self):
        self.advance()
        self.__ws()
    def match(self, para):
        if para == self.cur_char:
            self.consume()
        else:
            raise Exception("expect " + self.cur_char + " found " + para)
    def next_token(self):
        pass
    def get_token_name(self, token_type):
        pass
    def advance(self):
        self.cur_index += 1
        if self.cur_index >= len(self.input_str):
            self.cur_char = lexer.const_eof
        else:
            self.cur_char = self.input_str[self.cur_index]
    def __ws(self):
        pass

if __name__ == '__main__':
    print("this is the lexer class def")