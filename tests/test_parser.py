# -*- coding: utf-8 -*-
# test_scanner.py
#
# author: Christopher S. Corley

from context import (recognizer, environment, parser, lexer, Types)

import unittest
from io import StringIO

class ParserTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_valid_files_parsed(self):
        with open("tests/case/abs.swl") as f:
            l = lexer.Lexer(f)
            p = parser.Parser(l)
            tree = p.program()

            assert tree
            print(tree)


    def test_parse_tree_empty(self):
        s = StringIO("")
        l = lexer.Lexer(s)
        p = parser.Parser(l)
        tree = p.program()

        assert tree is None

    def test_parse_tree_single_var(self):
        s = StringIO("var\n")
        l = lexer.Lexer(s)
        p = parser.Parser(l)
        with self.assertRaises(environment.EnvironmentError):
            tree = p.program()

    def test_parse_tree_def(self):
        s = StringIO("def var:\n    5\n")
        l = lexer.Lexer(s)
        p = parser.Parser(l)
        tree = p.program()

        assert tree
        assert tree.val_type == Types.form_list
        assert tree.left
        assert tree.left.val_type == Types.JOIN
        assert tree.left.left
        def_tree = tree.left.left
        assert def_tree.val_type == Types.kw_def
        assert def_tree.left
        assert def_tree.right
        assert def_tree.left.val_type == Types.variable
        assert def_tree.right.val_type == Types.colon
        assert def_tree.right.left.val_type == Types.newline
        assert def_tree.right.right
        def_body = def_tree.right.right
        assert def_body.val_type == Types.form_list
        assert def_body.left
        assert def_body.left.val_type == Types.JOIN
        assert def_body.left.left.val_type == Types.integer
        assert def_body.left.left.val == "5"
        assert def_body.left.right.val_type == Types.newline

    def test_parse_tree_def_lambda(self):
        s = StringIO("def identity:\n    lambda(x):\n      x\n")
        l = lexer.Lexer(s)
        p = parser.Parser(l)
        tree = p.program()

        assert tree
        print(tree)
        assert tree.val_type == Types.form_list


if __name__ == '__main__':
    unittest.main()
