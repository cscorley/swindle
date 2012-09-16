# -*- coding: utf-8 -*-

from .context import swindle

import unittest

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_life_universe_and_everything(self):
        answer = 42

        assert answer == 42


if __name__ == '__main__':
    unittest.main()
