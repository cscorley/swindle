# -*- coding: utf-8 -*-
# test_scanner.py
#
# author: Christopher S. Corley

from context import scanner

import unittest
from io import StringIO

class ScannerTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_valid_files_scanned(self):
        assert scanner.scan("tests/case/emptyfile") is True
        assert scanner.scan("tests/case/abs.swl") is True
        assert scanner.scan("tests/case/mystring.swl") is True
        assert scanner.scan("tests/case/factorial.swl") is True
        assert scanner.scan("tests/case/mandelbrot.swl") is True

    def test_invalid_files_caught(self):
        assert scanner.scan(None) is False
        assert scanner.scan("") is False
        assert scanner.scan("/") is False
        assert scanner.scan("C:\\") is False
        assert scanner.scan(2) is False
        assert scanner.scan("""Docstring yo""") is False
        assert scanner.scan(list()) is False
        assert scanner.scan(dict()) is False

    def test_lexemes_print_to_StringIO(self):
        strio = StringIO("")
        assert scanner.scan("tests/case/abs.swl", strio) is True





if __name__ == '__main__':
    unittest.main()
