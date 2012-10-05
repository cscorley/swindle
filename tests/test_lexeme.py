# -*- coding: utf-8 -*-

from context import (
        lexeme,
        Types,
        KEYWORDS,
        PUNCTUATION,
        LITERALS_PUNC)

import unittest
from io import StringIO

class LexemeTestSuite(unittest.TestCase):

    def test_punctuation(self):
        """Make sure we return correct punctuation lexemes"""

        for item in PUNCTUATION:
            l = lexeme.Lexeme(item, 0, 0)
            assert l.val == item
            assert l.val_type is Types.punctuation

    def test_literal_punctuation(self):
        """Make sure we return correct literals punctuation lexemes"""

        for item in LITERALS_PUNC:
            l = lexeme.Lexeme(item, 0, 0)
            assert l.val == item
            assert l.val_type is Types.literals_punc

    def test_keywords(self):
        """Make sure we return correct keyword lexemes"""

        for item in KEYWORDS:
            l = lexeme.Lexeme(item, 0, 0)
            assert l.val == item

            if item == "True" or item == "False":
                assert l.val_type is Types.boolean
            else:
                assert l.val_type is Types.keyword

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
