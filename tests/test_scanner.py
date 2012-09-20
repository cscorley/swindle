# -*- coding: utf-8 -*-

from context import scanner

import unittest

class ScannerTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_valid_files_scanned(self):
        assert scanner.scan("tests/case/emptyfile") is True

    def test_invalid_files_caught(self):
        assert scanner.scan("") is False
        assert scanner.scan("C:\\") is False
        assert scanner.scan(2) is False
        assert scanner.scan("""Docstring yo""") is False
        assert scanner.scan(list()) is False
        assert scanner.scan(dict()) is False



if __name__ == '__main__':
    unittest.main()
