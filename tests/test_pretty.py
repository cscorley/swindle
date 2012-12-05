# -*- coding: utf-8 -*-
# test_pretty.py
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

    def test_pretty_quote_symbol(self):
        s = StringIO("def s:\n  `symbol\n")
        l = lexer.Lexer(s)
        p = parser.Parser(l)
        tree = p.program()
        pstr = pretty.make_pretty(tree)

        cstr = "def s:\n    `symbol\n"
        print(pstr)
        print(cstr)
        assert pstr == cstr


    def test_pretty_def(self):
        s = StringIO("def var:\n  5\n")
        l = lexer.Lexer(s)
        p = parser.Parser(l)
        tree = p.program()
        pstr = pretty.make_pretty(tree)

        print(pstr)
        assert pstr == "def var:\n    5\n"

    def test_pretty_def_lambda(self):
        s = StringIO("def identity:\n lambda x:\n              x\n")
        l = lexer.Lexer(s)
        p = parser.Parser(l)
        tree = p.program()
        pstr = pretty.make_pretty(tree)

        assert pstr == "def identity:\n    lambda x:\n        x\n"

    def test_pretty_case_mandelbrot(self):
        with open("tests/case/mandelbrot.swl") as s:
            l = lexer.Lexer(s)
            p = parser.Parser(l)
            tree = p.program()
            pstr = pretty.make_pretty(tree)

            cstr = "def square:\n    lambda x:\n        mul(x x)\ndef mandelbrot_iter:\n    lambda iterations:\n        lambda x y:\n            def helper:\n                lambda iter_left r s:\n                    if equal(iter_left 0):\n                        0\n                    elif gt(sqrt(add(square(r) square(s))) 2):\n                        sub(iterations iter_left)\n                    else:\n                        helper(sub(iter_left 1) add(sub(square(r) square(s)) x) add(mul(2 r s) y))\n            helper(iterations 0 0)\n"
            print(pstr)
            print(cstr)
            assert pstr == cstr

    def test_pretty_case_tuples(self):
        with open("tests/case/tuple.swl") as s:
            l = lexer.Lexer(s)
            p = parser.Parser(l)
            tree = p.program()
            pstr = pretty.make_pretty(tree)

            cstr = 'def a_tuple:\n    `["Item1" 2 ["Nested" "Tuples"] 3 4]\nprint(a_tuple)\n'
            print(pstr)
            print(cstr)
            assert pstr == cstr




if __name__ == '__main__':
    unittest.main()
