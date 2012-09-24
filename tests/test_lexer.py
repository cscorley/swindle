# -*- coding: utf-8 -*-

from context import lexer
from context import lexeme

import unittest
from io import StringIO

class LexerTestSuite(unittest.TestCase):

    def test_sets_indention_level(self):
        """Make sure the indention level remains a positive int."""
        l = lexer.Lexer(StringIO(""))
        assert l.indent_count == 0

        with self.assertRaises(Exception):
            l.indent_count = ""
            l.indent_count = -1

    def test_punctuation_lexes(self):
        """Make sure we return correct punctuation lexemes"""


        l = lexer.Lexer(StringIO(":()[]+-`"))
        lexeme = l.lex()
        assert lexeme.val == ":"
        lexeme = l.lex()
        assert lexeme.val == "("
        lexeme = l.lex()
        assert lexeme.val == ")"
        lexeme = l.lex()
        assert lexeme.val == "["
        lexeme = l.lex()
        assert lexeme.val == "]"
        lexeme = l.lex()
        assert lexeme.val == "+"
        lexeme = l.lex()
        assert lexeme.val == "-"
        lexeme = l.lex()
        assert lexeme.val == "`"


if __name__ == '__main__':
    unittest.main()
