import os
import sys

from swindle.lexer import Lexer

def scan(source, destination=sys.stdout):
    if type(source) != str or len(source) == 0:
        return False

    try:
        with open(source) as f:
            lexer = Lexer(f)

            token = lexer.lex()
            while token:
                destination.write(str(token))
                destination.write('\n')
                token = lexer.lex()
    except IOError as e:
        destination.write(str(e))
        destination.write('\n')
        return False

    return True
