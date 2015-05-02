__author__ = 'ray'
from ListParser import ListParser
from ListLexer import ListLexer
#input_str = raw_input()
while 1:
    input_str = '[a,a,'
    lexer = ListLexer(input_str)
    parser = ListParser(lexer, 3)
    parser.list()
    #input_str = sys.stdin.readline()
    #input_str = raw_input()