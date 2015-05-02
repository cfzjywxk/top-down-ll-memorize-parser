__author__ = 'ray'
from ListParser import ListParser
from ListLexer import ListLexer
input_str = raw_input()
while input_str:
    #input_str = '[a,b]'
    lexer = ListLexer(input_str)
    parser = ListParser(lexer)
    parser.list()
    #input_str = sys.stdin.readline()
    input_str = raw_input()