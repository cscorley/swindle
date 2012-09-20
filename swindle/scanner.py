import os
import sys

from swindle.lexer import Lexer

def scan(filename): 
    if type(filename) != str or len(filename) == 0:
        return False
    
    try:
        with open(filename) as f:
            lexer = Lexer(f)

            for token in lexer.lex():
                print(token)
    except IOError as e:
        print(e)
        return False

    return True
