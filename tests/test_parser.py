# -*- coding: utf-8 -*-
# test_scanner.py
#
# author: Christopher S. Corley

from context import (recognizer, parser, lexer, Types)

import unittest
from io import StringIO

class ParserTestSuite(unittest.TestCase):
    """Basic test cases."""

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
        tree = p.program()

        assert tree
        assert tree.val_type == Types.JOIN
        assert tree.left
        assert tree.left.val_type == Types.JOIN
        assert tree.left.left
        assert tree.left.right
        assert tree.left.left.val_type == Types.variable
        assert tree.left.right.val_type == Types.newline

    def test_parse_tree_def(self):
        s = StringIO("def var:\n    5\n")
        l = lexer.Lexer(s)
        p = parser.Parser(l)
        tree = p.program()

        assert tree
        assert tree.val_type == Types.JOIN
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




if __name__ == '__main__':
    unittest.main()
