# scanner.py
#
# author: Christopher S. Corley

import os
import sys

from swindle.lexer import Lexer
from swindle.parser import Parser

def parse_file(source, destination=sys.stdout):
    if type(source) != str or len(source) == 0:
        return False

    try:
        with open(source) as f:
            lexer = Lexer(f)
            parser = Parser(lexer)
            parser.program()

    except IOError as e:
        destination.write(str(e))
        destination.write('\n')
        return False

    return True
