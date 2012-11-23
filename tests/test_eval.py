# -*- coding: utf-8 -*-
# test_scanner.py
#
# author: Christopher S. Corley

from context import (evaluator, recognizer, environment, parser, lexer, Types)

import unittest
from io import StringIO

class EvaluatorTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_valid_files_parsed(self):
        assert evaluator.eval_file("tests/case/emptyfile") is True
        assert evaluator.eval_file("swindle/library/main.swl") is True
        assert evaluator.eval_file("tests/case/abs.swl") is True
        assert evaluator.eval_file("tests/case/mystring.swl") is True
        assert evaluator.eval_file("tests/case/annoying.swl") is True
        assert evaluator.eval_file("tests/case/tuple.swl") is True
        assert evaluator.eval_file("tests/case/factorial.swl") is True
        assert evaluator.eval_file("tests/case/mandelbrot.swl") is True


if __name__ == '__main__':
    unittest.main()
