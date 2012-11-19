# pretty.py
#
# author: Christopher S. Corley

import os
import sys

from swindle.lexer import Lexer
from swindle.parser import Parser
from swindle.types import Types

def make_pretty(tree):
    if tree is None:
        return ""

    t = tree.val_type
    pstr = str()
    if t == Types.kw_def:
        pstr += "def"
    elif t == Types.kw_lambda:
        pstr += "lambda"
    elif t == Types.kw_set:
        pstr += "set!"
    elif t == Types.kw_if:
        pstr += "if"
    elif t == Types.kw_elif:
        pstr += "elif"
    elif t == Types.kw_else:
        pstr += "else"
    elif t == Types.colon:
        pstr += ":"
    elif t == Types.oparen:
        pstr += "("
    elif t == Types.cparen:
        pstr += ")"
    elif t == Types.obracket:
        pstr += "["
    elif t == Types.cbracket:
        pstr += "]"
    elif t == Types.quote:
        pstr += "`"
    elif t == Types.newline:
        pstr += "\n"
    elif t == Types.integer:
        pstr += str(tree.val)
    elif t == Types.string:
        pstr += str(tree.val)
    elif t == Types.variable:
        pstr += str(tree.val)
    elif t == Types.JOIN:
        pstr += make_pretty(tree.left) + make_pretty(tree.right)
    else:
        raise Exception("Can't make this ugly thing pretty.")

    return pstr


def pretty_file(source, destination=sys.stdout):
    if type(source) != str or len(source) == 0:
        return False

    try:
        with open(source) as f:
            lexer = Lexer(f)
            parser = Parser(lexer)
            tree = parser.program()
            pretty_string = make_pretty(tree)
            destintation.write(pretty_string)

    except IOError as e:
        destination.write(str(e))
        destination.write('\n')
        return False

    return True
