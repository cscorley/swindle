# -*- coding: utf-8 -*-
# test_lexer.py
#
# author: Christopher S. Corley

from context import (
        lexer,
        Types)

import unittest
from io import StringIO

class LexerTestSuite(unittest.TestCase):

    def test_newlines(self):
        l = lexer.Lexer(StringIO("0\n"))
        lexeme = l.lex()
        assert lexeme.val == "0"
        assert lexeme.val_type is Types.integer
        lexeme = l.lex()
        assert lexeme.val == "\n"
        assert lexeme.val_type is Types.newline

        l = lexer.Lexer(StringIO("\"String\"\n"))
        lexeme = l.lex()
        assert lexeme.val == "\"String\""
        assert lexeme.val_type is Types.string
        lexeme = l.lex()
        assert lexeme.val == "\n"
        assert lexeme.val_type is Types.newline

        l = lexer.Lexer(StringIO("def\n"))
        lexeme = l.lex()
        assert lexeme.val == "def"
        assert lexeme.val_type is Types.kw_def
        lexeme = l.lex()
        assert lexeme.val == "\n"
        assert lexeme.val_type is Types.newline

        l = lexer.Lexer(StringIO("\n\ndef\n"))
        lexeme = l.lex()
        assert lexeme.val == "def"
        assert lexeme.val_type is Types.kw_def
        lexeme = l.lex()
        assert lexeme.val == "\n"
        assert lexeme.val_type is Types.newline

        l = lexer.Lexer(StringIO("True\n"))
        lexeme = l.lex()
        assert lexeme.val == "True"
        assert lexeme.val_type is Types.variable
        lexeme = l.lex()
        assert lexeme.val == "\n"
        assert lexeme.val_type is Types.newline


    def test_invalid_variables_caught(self):
        l = lexer.Lexer(StringIO("1adder"))
        with self.assertRaises(Exception):
            l.lex()

        l = lexer.Lexer(StringIO("set?"))
        with self.assertRaises(Exception):
            l.lex()

    def test_strings(self):
        """Make sure confusing strings work"""

        test1 = "\"This is a test string\""
        l = lexer.Lexer(StringIO(test1))
        lexeme = l.lex()
        assert lexeme.val == test1
        assert lexeme.val_type is Types.string

        test2 = "\"This string has an embedded \\\"string\\\"\""
        l = lexer.Lexer(StringIO(test2))
        lexeme = l.lex()
        assert lexeme.val == test2
        assert lexeme.val_type is Types.string

        test3 = "\"This string has escaped\n\t\f characters \""
        l = lexer.Lexer(StringIO(test3))
        lexeme = l.lex()
        assert lexeme.val == test3
        assert lexeme.val_type is Types.string

        l = lexer.Lexer(StringIO(test1 + test2))
        lexeme = l.lex()
        assert lexeme.val == test1
        lexeme = l.lex()
        assert lexeme.val == test2

    def test_case_abs(self):
        """tests/case/abs.swl"""

        """
def abs:
    lambda x:
        if ( lt(x 0) ):
            -x
        else:
            x

abs(-4)
"""

        with open('tests/case/abs.swl') as f:
            l = lexer.Lexer(f)

            lexeme = l.lex()
            assert lexeme.val == "def"

            lexeme = l.lex()
            assert lexeme.val == "abs"
            assert lexeme.val_type is Types.variable

            lexeme = l.lex()
            assert lexeme.val == ":"

            lexeme = l.lex()
            assert lexeme.val_type is Types.newline

            lexeme = l.lex()
            assert lexeme.val == "lambda"

            lexeme = l.lex()
            assert lexeme.val == "x"
            assert lexeme.val_type is Types.variable

            lexeme = l.lex()
            assert lexeme.val == ":"

            lexeme = l.lex()
            assert lexeme.val_type is Types.newline

            lexeme = l.lex()
            assert lexeme.val == "if"

            lexeme = l.lex()
            assert lexeme.val == "lt"
            assert lexeme.val_type is Types.variable

            lexeme = l.lex()
            assert lexeme.val == "("

            lexeme = l.lex()
            assert lexeme.val == "x"
            assert lexeme.val_type is Types.variable

            lexeme = l.lex()
            assert lexeme.val == "0"
            assert lexeme.val_type is Types.integer

            lexeme = l.lex()
            assert lexeme.val == ")"

            lexeme = l.lex()
            assert lexeme.val == ":"

            lexeme = l.lex()
            assert lexeme.val_type is Types.newline

            lexeme = l.lex()
            assert lexeme.val == "neg"
            assert lexeme.val_type is Types.variable

            lexeme = l.lex()
            assert lexeme.val == "("
            lexeme = l.lex()
            assert lexeme.val == "x"
            assert lexeme.val_type is Types.variable
            lexeme = l.lex()
            assert lexeme.val == ")"

            lexeme = l.lex()
            assert lexeme.val_type is Types.newline


            lexeme = l.lex()
            assert lexeme.val == "else"

            lexeme = l.lex()
            assert lexeme.val == ":"

            lexeme = l.lex()
            assert lexeme.val_type is Types.newline


            lexeme = l.lex()
            assert lexeme.val == "x"
            assert lexeme.val_type is Types.variable

            lexeme = l.lex()
            assert lexeme.val_type is Types.newline

            lexeme = l.lex()
            assert lexeme.val == "print"
            assert lexeme.val_type is Types.variable

            lexeme = l.lex()
            assert lexeme.val == "("

            lexeme = l.lex()
            assert lexeme.val == "abs"
            assert lexeme.val_type is Types.variable

            lexeme = l.lex()
            assert lexeme.val == "("

            lexeme = l.lex()
            assert lexeme.val == "neg"
            assert lexeme.val_type is Types.variable

            lexeme = l.lex()
            assert lexeme.val == "("

            lexeme = l.lex()
            assert lexeme.val == "4"
            assert lexeme.val_type is Types.integer

            lexeme = l.lex()
            assert lexeme.val == ")"

            lexeme = l.lex()
            assert lexeme.val == ")"

            lexeme = l.lex()
            assert lexeme.val == ")"


            lexeme = l.lex()
            assert lexeme.val_type is Types.newline

if __name__ == '__main__':
    unittest.main()
