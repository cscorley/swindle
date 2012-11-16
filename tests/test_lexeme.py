# -*- coding: utf-8 -*-
# test_lexeme.py
#
# author: Christopher S. Corley

from context import (
        lexeme,
        Types,
        )

import unittest
from io import StringIO

class LexemeTestSuite(unittest.TestCase):

    def test_punctuation(self):
        """Make sure we return correct punctuation lexemes"""

        item = ':'
        l = lexeme.Lexeme(item, 0, 0)
        assert l.val == item
        assert l.val_type is Types.colon

        item = '('
        l = lexeme.Lexeme(item, 0, 0)
        assert l.val == item
        assert l.val_type is Types.oparen

        item = ')'
        l = lexeme.Lexeme(item, 0, 0)
        assert l.val == item
        assert l.val_type is Types.cparen

    def test_literal_punctuation(self):
        """Make sure we return correct literals punctuation lexemes"""

        item = '['
        l = lexeme.Lexeme(item, 0, 0)
        assert l.val == item
        assert l.val_type is Types.obracket

        item = ']'
        l = lexeme.Lexeme(item, 0, 0)
        assert l.val == item
        assert l.val_type is Types.cbracket

        item = '`'
        l = lexeme.Lexeme(item, 0, 0)
        assert l.val == item
        assert l.val_type is Types.quote

    def test_keywords(self):
        """Make sure we return correct keyword lexemes"""

        item = 'def'
        l = lexeme.Lexeme(item, 0, 0)
        assert l.val == item
        assert l.val_type is Types.kw_def

        item = 'lambda'
        l = lexeme.Lexeme(item, 0, 0)
        assert l.val == item
        assert l.val_type is Types.kw_lambda

        item = 'set!'
        l = lexeme.Lexeme(item, 0, 0)
        assert l.val == item
        assert l.val_type is Types.kw_set

        item = 'if'
        l = lexeme.Lexeme(item, 0, 0)
        assert l.val == item
        assert l.val_type is Types.kw_if

        item = 'elif'
        l = lexeme.Lexeme(item, 0, 0)
        assert l.val == item
        assert l.val_type is Types.kw_elif

        item = 'else'
        l = lexeme.Lexeme(item, 0, 0)
        assert l.val == item
        assert l.val_type is Types.kw_else

    def test_literals(self):
        """Make sure literals get the correct type"""

        item = '20'
        l = lexeme.Lexeme(item, 0, 0)
        assert l.val == item
        assert l.val_type is Types.integer

        item = '"Some string"'
        l = lexeme.Lexeme(item, 0, 0)
        assert l.val == item
        assert l.val_type is Types.string

        item = 'blah'
        l = lexeme.Lexeme(item, 0, 0)
        assert l.val == item
        assert l.val_type is Types.variable

    def test_invalid_lexeme_children(self):
        """Make sure Lexeme doesn't allow invalid children"""

        l = lexeme.Lexeme("", 0, 0)
        assert l.right == None
        assert l.left == None

        with self.assertRaises(Exception):
            l.left = "Something"
            l.right = 6
            l.left = l
            l.right = l


if __name__ == '__main__':
    unittest.main()
