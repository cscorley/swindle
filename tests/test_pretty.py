# -*- coding: utf-8 -*-
# test_scanner.py
#
# author: Christopher S. Corley

from context import (pretty, recognizer, environment, parser, lexer, Types)

import unittest
from io import StringIO

class PrettyTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_valid_files_parsed(self):
        with open("tests/case/abs.swl") as f:
            l = lexer.Lexer(f)
            p = parser.Parser(l)
            tree = p.program()

            assert tree
            print(tree)


    def test_pretty_tree_empty(self):
        s = StringIO("")
        l = lexer.Lexer(s)
        p = parser.Parser(l)
        tree = p.program()
        pstr = pretty.make_pretty(tree)

        print(pstr)
        assert pstr == ""


    def test_pretty_def(self):
        s = StringIO("def var:\n  5\n")
        l = lexer.Lexer(s)
        p = parser.Parser(l)
        tree = p.program()
        pstr = pretty.make_pretty(tree)

        print(pstr)
        assert pstr == "def var:\n    5\n"

    def test_pretty_def_lambda(self):
        s = StringIO("def identity:\n lambda(x):\n              x\n")
        l = lexer.Lexer(s)
        p = parser.Parser(l)
        tree = p.program()
        pstr = pretty.make_pretty(tree)

        print(pstr)
        assert pstr == "def identity:\n    lambda(x):\n        x\n"


if __name__ == '__main__':
    unittest.main()
