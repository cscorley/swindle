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

    def test_creation(self):
        e = environment.Environment(debug=LUSTH)
        assert type(e) == environment.Environment

    def test_insertion(self):
        e = environment.Environment(debug=LUSTH)
        e.env_insert('blah', 1)
        assert 'blah' in e
        assert e['blah'] == 1

        e.env_insert('bleh', 'tacos!')
        assert 'bleh' in e
        assert e['bleh'] == 'tacos!'

        with self.assertRaises(environment.EnvironmentError):
            e.env_insert(None, None)
        assert None not in e


    def test_lookup(self):
        e = environment.Environment(debug=LUSTH)

    def test_update(self):
        e = environment.Environment(debug=LUSTH)

    def test_extend(self):
        e = environment.Environment(debug=LUSTH)




if __name__ == '__main__':
    LUSTH = True # LOLOLOLOL
    #unittest.main(verbosity=0)
    unittest.main()
