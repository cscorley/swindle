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
        assert tree.right is None

        assert tree.left.val_type == Types.form
        assert tree.left.left
        assert tree.left.right is None

        def_tree = tree.left.left
        assert def_tree.val_type == Types.kw_def
        assert def_tree.left
        assert def_tree.right
        assert def_tree.left.val_type == Types.variable
        assert def_tree.right.val_type == Types.colon

        assert def_tree.right.left
        assert def_tree.right.right
        assert def_tree.right.left.val_type == Types.newline

        def_body = def_tree.right.right
        assert def_body.val_type == Types.form_list
        assert def_body.left
        assert def_body.right is None

        assert def_body.left.val_type == Types.form
        assert def_body.left.left
        assert def_body.left.right

        assert def_body.left.left.val_type == Types.integer
        assert def_body.left.left.val == "5"
        assert def_body.left.right.val_type == Types.newline


    def test_parse_tree_def_lambda(self):
        s = StringIO("def identity:\n    lambda x:\n      x\n")
        l = lexer.Lexer(s)
        p = parser.Parser(l)
        tree = p.program()

        assert tree
        assert tree.val_type == Types.form_list
        assert tree.left
        assert tree.right is None

        assert tree.left.val_type == Types.form
        assert tree.left.left
        assert tree.left.right is None

        def_tree = tree.left.left
        assert def_tree.val_type == Types.kw_def
        assert def_tree.left
        assert def_tree.right
        assert def_tree.left.val_type == Types.variable
        assert def_tree.left.val == "identity"
        assert def_tree.right.val_type == Types.colon

        assert def_tree.right.left
        assert def_tree.right.right
        assert def_tree.right.left.val_type == Types.newline

        def_body = def_tree.right.right
        assert def_body.val_type == Types.form_list
        assert def_body.left
        assert def_body.right is None

        assert def_body.left.val_type == Types.form
        assert def_body.left.left
        assert def_body.left.left.val_type == Types.kw_lambda

        lambda_tree = def_body.left.left
        assert lambda_tree.left
        assert lambda_tree.right
        assert lambda_tree.left.val_type == Types.parameter_list
        assert lambda_tree.left.left.val_type == Types.variable
        assert lambda_tree.left.left.val == "x"
        assert lambda_tree.left.right is None

        assert lambda_tree.right.val_type == Types.colon
        assert lambda_tree.right.left.val_type == Types.newline

        lambda_body = lambda_tree.right.right
        assert lambda_body.val_type == Types.form_list
        assert lambda_body.left
        assert lambda_body.right is None

        assert lambda_body.left.val_type == Types.form
        assert lambda_body.left.left
        assert lambda_body.left.left.val_type == Types.variable
        assert lambda_body.left.left.val == "x"
        assert lambda_body.left.right.val_type == Types.newline

    def test_parse_tree_quote_symbol(self):
        s = StringIO("def s:\n  `symbol\n")
        l = lexer.Lexer(s)
        p = parser.Parser(l)
        tree = p.program()

        assert tree
        assert tree.val_type == Types.form_list
        assert tree.left
        assert tree.right is None

        assert tree.left.val_type == Types.form
        assert tree.left.left
        assert tree.left.right is None

        def_tree = tree.left.left
        assert def_tree.val_type == Types.kw_def
        assert def_tree.left
        assert def_tree.right
        assert def_tree.left.val_type == Types.variable
        assert def_tree.left.val == "s"
        assert def_tree.right.val_type == Types.colon

        assert def_tree.right.left
        assert def_tree.right.right
        assert def_tree.right.left.val_type == Types.newline

        def_body = def_tree.right.right
        assert def_body.val_type == Types.form_list
        assert def_body.left
        assert def_body.right is None

        assert def_body.left.val_type == Types.form
        assert def_body.left.left
        assert def_body.left.right

        assert def_body.left.left.val_type == Types.quote
        assert def_body.left.left.right.val_type == Types.symbol
        assert def_body.left.left.right.val == "symbol"
        assert def_body.left.left.left is None
        assert def_body.left.right.val_type == Types.newline

if __name__ == '__main__':
    unittest.main()
