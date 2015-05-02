__author__ = 'ray'
from ListParser import ListParser
from ListLexer import ListLexer
input_str = raw_input()
while 1:
    #input_str = '[a,a,'
    lexer = ListLexer(input_str)
    parser = ListParser(lexer)
    parser.stat()
    #input_str = sys.stdin.readline()
    input_str = raw_input()