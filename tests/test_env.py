# -*- coding: utf-8 -*-
# test_environment.py
#
# author: Christopher S. Corley

from context import environment

import unittest
from io import StringIO

LUSTH=False

class EnvironmentTestSuite(unittest.TestCase):
    """Basic test cases."""

    def __init__(self, methodName='runTest', lusth=False):
        LUSTH = lusth
        super(EnvironmentTestSuite, self).__init__(methodName=methodName)

    def test_setup(self):
        e = environment.Environment(debug=LUSTH)
        assert type(e) == environment.Environment
#        assert e.debug == False
        e = environment.Environment(debug=LUSTH)
        e = environment.Environment(debug=LUSTH)
        e = environment.Environment(debug=LUSTH)
        e = environment.Environment(debug=LUSTH)
        e = environment.Environment(debug=LUSTH)
        pass

if __name__ == '__main__':
    LUSTH = True # LOLOLOLOL
    #unittest.main(verbosity=0)
    unittest.main()
