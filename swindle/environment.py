# environment.py
#
# author: Christopher S. Corley

import pprint
from swindle.builtins import (Closure, Plosure)
import swindle.builtins as swndl
import math

class EnvironmentError(Exception):
     def __init__(self, value):
         self.message = value
     def __str__(self):
         return str(self.message)

class EnvironmentLookupError(EnvironmentError):
    pass

class Environment(dict):
    def __init__(self, iterable=None, parent=None):
        self.parent = parent
        self.depth = 0

        if self.parent:
            self.depth = self.parent.depth + 1

        if iterable:
            super(Environment, self).__init__(iterable)

    def env_display(self):
        print('Environment %d:' % self.depth)
        pprint.pprint(self, indent=4, width=50)

        if self.parent:
            self.parent.env_display()

        print('')

    def env_lookup(self, variable):
        if variable in self:
            return self[variable]
        elif self.parent:
            return self.parent.env_lookup(variable)
        else:
            raise EnvironmentLookupError("Variable '%s' is unbound in the environment" % variable)

    def env_update(self, variable, value):
        if variable in self:
            old = self[variable]
            self[variable] = value
        elif self.parent:
            old = self.parent.env_update(variable, value)
        else:
            raise EnvironmentError("Variable is unbound in the environment")

        return old

    def env_insert(self, variable, value):
        if type(variable) != str:
            raise EnvironmentError("What are you doing?")

        if variable in self:
            raise EnvironmentError("Variable is already bound in this environment")
        else:
            self[variable] = value

        return value

    def env_extend(self, pairs=[]):
        return Environment(pairs, parent=self)


class DebugEnvironment(Environment):
    def __init__(self, iterable=None, parent=None):
        self.parent = parent
        self.depth = 0
        print("\n\n")
        if self.parent:
            print("Creating new local environment")
        else:
            print("Creating a new environment")

        if iterable:
            super(DebugEnvironment, self).__init__(iterable=iterable, parent=parent)

        self.env_display()

    def env_lookup(self, variable):
        print("(%d) Looking up variable %s ... " % (self.depth, str(variable)), end='')
        val = super(DebugEnvironment, self).env_lookup(variable)
        print("found %s:%s" % (str(variable), str(val)))
        self.env_display()
        return val

    def env_update(self, variable, value):
        self.env_display()
        print("(%d) Updating variable %s with value %s ... " % (self.depth, str(variable), str(value)), end='')
        val = super(DebugEnvironment, self).env_update(variable, value)
        print("replaced %s:%s" % (str(variable), str(val)))
        self.env_display()
        return val

    def env_insert(self, variable, value):
        print("(%d) Inserting variable %s with value %s ... " % (self.depth, str(variable), str(value)), end='')
        val = super(DebugEnvironment, self).env_insert(variable, value)
        print("inserted %s:%s" % (str(variable), str(val)))
        self.env_display()
        return val

    def env_extend(self, pairs=[]):
        print("(%d) Extending environment with %s ... " % (self.depth, str(pairs)), end='')
        val = DebugEnvironment(pairs, parent=self)
        print(" ... success")
        val.env_display()
        return val

class SetupEnvironment(Environment):
    def __init__(self, args=[]):
        self.args = args
        iterable = [
            ('False', False),
            ('True', True),
            ('None', None),
            ('len', Plosure(len)),
            ('str', Plosure(str)),
            ('int', Plosure(int)),
            ('print', Plosure(print)),
            ('input', Plosure(swndl.reader)),
            ('args', Plosure(self.argv_swndl)),

            # lisp
            ('cons', Plosure(swndl.cons)),
            ('car', Plosure(swndl.car)),
            ('cdr', Plosure(swndl.cdr)),
            ('list', Plosure(swndl.make_list)),
            ('array', Plosure(swndl.make_array)),
            ('set_car', Plosure(swndl.set_car)),
            ('set_cdr', Plosure(swndl.set_cdr)),
            ('get_item', Plosure(swndl.get_item)),
            ('set_item', Plosure(swndl.set_item)),


            # maths
            ('neg', Plosure(swndl.neg)),
            ('equal', Plosure(swndl.equal)),
            ('lt', Plosure(swndl.lt)),
            ('gt', Plosure(swndl.gt)),
            ('add', Plosure(swndl.add)),
            ('sub', Plosure(swndl.sub)),
            ('mul', Plosure(swndl.mul)),
            ('div', Plosure(swndl.div)),
            ('and', Plosure(swndl.and_op)),
            ('or', Plosure(swndl.or_op)),
            ('not', Plosure(swndl.not_op)),

            ('cos', Plosure(math.cos)),
            ('sin', Plosure(math.sin)),
            ('log', Plosure(math.log)),
            ('tan', Plosure(math.tan)),
            ('pow', Plosure(math.pow)),
            ('factorial', Plosure(math.factorial)),
            ('sqrt', Plosure(math.sqrt)),

            # objects
            ('new', Plosure(swndl.new)),
            ]

        super(SetupEnvironment, self).__init__(iterable)

    def argv_swndl(self):
        return self.args
