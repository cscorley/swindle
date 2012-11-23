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
        with open("tests/case/mystring.swl") as f:
            l = lexer.Lexer(f)
            p = parser.Parser(l)
            tree = p.program()
            e = evaluator.Evaluator()
            et = e.eval(tree, e.global_env.env_extend())

            print(et)
            assert tree
            assert et
            assert False



if __name__ == '__main__':
    unittest.main()
