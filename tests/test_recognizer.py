# -*- coding: utf-8 -*-
# test_scanner.py
#
# author: Christopher S. Corley

from context import (recognizer, parser)

import unittest
from io import StringIO

class RecognizerTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_valid_files_parsed(self):
        assert recognizer.parse_file("tests/case/abs.swl") is True
        assert recognizer.parse_file("tests/case/mystring.swl") is True
        assert recognizer.parse_file("tests/case/factorial.swl") is True
        assert recognizer.parse_file("tests/case/mandelbrot.swl") is True
        assert recognizer.parse_file("tests/case/annoying.swl") is True
        assert recognizer.parse_file("tests/case/tuple.swl") is True
        assert recognizer.parse_file("tests/case/emptyfile") is True

    def test_invalid_files_parsed(self):
        with self.assertRaises(parser.ParseError):
            recognizer.parse_file("tests/case/bad_abs.swl")

        with self.assertRaises(parser.ParseError):
            recognizer.parse_file("tests/case/bad_mystring.swl")

        with self.assertRaises(parser.ParseError):
            recognizer.parse_file("tests/case/bad_factorial.swl")

        with self.assertRaises(parser.ParseError):
            recognizer.parse_file("tests/case/bad_factorial2.swl")

    def test_invalid_files_caught(self):
        assert recognizer.parse_file(None) is False
        assert recognizer.parse_file("") is False
        assert recognizer.parse_file("/") is False
        assert recognizer.parse_file("C:\\") is False
        assert recognizer.parse_file(2) is False
        assert recognizer.parse_file("""Docstring yo""") is False
        assert recognizer.parse_file(list()) is False
        assert recognizer.parse_file(dict()) is False


if __name__ == '__main__':
    unittest.main()
