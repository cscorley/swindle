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
        lexemes = [x for x in l.lex()]
        assert len(lexemes) != 0
        assert lexemes[0].val == ':'
        assert lexemes[1].val == "("
        assert lexemes[2].val == ")"
        assert lexemes[3].val == "["
        assert lexemes[4].val == "]"
        assert lexemes[5].val == "+"
        assert lexemes[6].val == "-"
        assert lexemes[7].val == "`"


if __name__ == '__main__':
    unittest.main()
