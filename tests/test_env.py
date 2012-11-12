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

    def setUp(self):
        if LUSTH:
            self.e0 = environment.DebugEnvironment(
                    [('blah1', 1)
                    ,('blah2', 2)
                    ,('blah3', 3)
                    ,('blah4', 4)
                    ,('blah5', 5)])
        else:
            self.e0 = environment.Environment(
                    [('blah1', 1)
                    ,('blah2', 2)
                    ,('blah3', 3)
                    ,('blah4', 4)
                    ,('blah5', 5)])

    def test_creation(self):
        e = environment.Environment()
        assert type(e) == environment.Environment
        assert len(e) == 0
        assert len(self.e0) == 5

    def test_insertion(self):
        e = self.e0
        assert e.env_insert('blah', 'bleh') == 'bleh'
        assert 'blah' in e
        assert e['blah'] == 'bleh'

        assert e.env_insert('bleh', 'tacos!') == 'tacos!'
        assert 'bleh' in e
        assert e['bleh'] == 'tacos!'

        with self.assertRaises(environment.EnvironmentError):
            e.env_insert(None, None)
        assert None not in e

        with self.assertRaises(environment.EnvironmentError):
            e.env_insert('blah1', 10)
        with self.assertRaises(environment.EnvironmentError):
            e.env_insert('blah2', 20)
        with self.assertRaises(environment.EnvironmentError):
            e.env_insert('blah3', 30)
        with self.assertRaises(environment.EnvironmentError):
            e.env_insert('blah4', 40)
        with self.assertRaises(environment.EnvironmentError):
            e.env_insert('blah5', 50)

    def test_lookup(self):
        e = self.e0
        assert e.env_lookup('blah1') == 1
        assert e.env_lookup('blah2') == 2
        assert e.env_lookup('blah3') == 3
        assert e.env_lookup('blah4') == 4
        assert e.env_lookup('blah5') == 5

    def test_update(self):
        e = self.e0
        assert e.env_lookup('blah1') == 1
        assert e.env_update('blah1', 'one') == 1
        assert e.env_lookup('blah1') == 'one'

        ne = e.env_extend([('blah2', 'two')])
        assert ne.env_lookup('blah2') == 'two'
        assert ne.env_update('blah2', 'TWO?!') == 'two'
        assert ne.env_lookup('blah2') == 'TWO?!'

        assert ne.env_lookup('blah3') == 3
        assert ne.env_update('blah3', 'three') == 3
        assert ne.env_lookup('blah3') == 'three'
        assert e.env_lookup('blah3') == 'three'


    def test_extend(self):
        """ TESTING """
        e = self.e0

        ne = e.env_extend([('blah1', 'one')])
        assert e.env_lookup('blah1') == 1
        assert e.env_lookup('blah2') == 2
        assert ne.env_lookup('blah1') == 'one'
        assert ne.env_lookup('blah2') == 2

        nne = ne.env_extend([('blah1', False)])
        assert nne.env_lookup('blah1') is False
        assert nne.env_lookup('blah2') == 2


if __name__ == '__main__':
    LUSTH = True # LOLOLOLOL
    unittest.main()
