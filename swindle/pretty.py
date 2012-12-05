# pretty.py
#
# author: Christopher S. Corley

import os
import sys

from swindle.lexer import Lexer
from swindle.parser import Parser
from swindle.types import Types

def make_pretty(tree, depth=0):
    cur_indent = 4*depth
    if tree is None:
        return ""

    t = tree.val_type
    pstr = " " * cur_indent
    assert len(pstr) % 4 == 0
    if t == Types.kw_def:
        pstr += "def "
        pstr += make_pretty(tree.left, depth=0) + make_pretty(tree.right, depth)
    elif t == Types.kw_lambda:
        pstr += "lambda"
        pstr += make_pretty(tree.left, depth=0) + make_pretty(tree.right, depth)
    elif t == Types.kw_set:
        pstr += "set! "
        pstr += make_pretty(tree.left, depth=0) + make_pretty(tree.right, depth)
    elif t == Types.kw_if:
        pstr += "if "
        pstr += make_pretty(tree.left, depth=0)
        pstr += make_pretty(tree.right, depth)
    elif t == Types.kw_elif:
        pstr += "elif "
        pstr += make_pretty(tree.left, depth=0)
        pstr += make_pretty(tree.right, depth)
    elif t == Types.kw_else:
        pstr += "else"
        pstr += make_pretty(tree.left, depth=0) + make_pretty(tree.right, depth)
    elif t == Types.colon:
        pstr = ":"
        pstr += make_pretty(tree.left, depth+1) + make_pretty(tree.right, depth+1)
    elif t == Types.form_list:
        pstr = make_pretty(tree.left, depth)

        if tree.right:
            pstr += make_pretty(tree.right, depth)

    elif t == Types.parameter_list:
        pstr = " " + make_pretty(tree.left, depth=0)
        if tree.right:
            pstr += make_pretty(tree.right, depth=0)
    elif t == Types.expr_list:
        pstr = make_pretty(tree.left, depth=0)
        if tree.right:
            pstr += " " + make_pretty(tree.right, depth=0)
    elif t == Types.datum_list:
        pstr = make_pretty(tree.left, depth=0)
        if tree.right:
            pstr += " " + make_pretty(tree.right, depth=0)
    elif t == Types.oparen:
        # if oparen, then we're in a param list
        # (conditionals don't pick up oparens)
        pstr = "("
        pstr += make_pretty(tree.right, depth=0)
        pstr += ")"
    elif t == Types.obracket:
        pstr += "["
        pstr += make_pretty(tree.right, depth)
        pstr += "]"
    elif t == Types.quote:
        pstr += "`"
        pstr += make_pretty(tree.right, depth=0)
    elif t == Types.newline:
        pstr = "\n"
    elif t == Types.integer:
        pstr += str(tree.val)
    elif t == Types.string:
        pstr += str(tree.val)
    elif t == Types.symbol:
        pstr += str(tree.val)
    elif t == Types.variable:
        pstr += str(tree.val)

        # proc_call
        if tree.left and tree.left.val_type == Types.oparen:
            pstr += "("
            pstr += make_pretty(tree.right, depth=0)
            pstr += ")"
        if tree.left and tree.left.val_type == Types.dot:
            pstr += "."
            pstr += make_pretty(tree.right, depth=0)
    elif t == Types.form:
        pstr = make_pretty(tree.left, depth) + make_pretty(tree.right, depth)
    elif t == Types.JOIN:
        pstr = make_pretty(tree.left, depth) + make_pretty(tree.right, depth)
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
            destination.write(pretty_string)

    except IOError as e:
        destination.write(str(e))
        destination.write('\n')
        return False

    return True
