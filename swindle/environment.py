# environment.py
#
# author: Christopher S. Corley

import pprint

class EnvironmentError(Exception):
     def __init__(self, value):
         self.message = value
     def __str__(self):
         return str(self.message)

class Environment(dict):
    def __init__(self, parent=False, debug=False):
        self.debug = debug
        self.parent = parent
        if self.debug:
            print("Creating a new environment")


    def env_display(self, depth=0, recurse=False):
        print('Environment %d:' % depth, end=' ')
        pprint.pprint(self)

        if recurse and self.parent:
            self.parent.env_display(depth=depth, recurse=recurse)

        print('')

    def env_lookup(self, variable):
        if self.debug:
            self.env_display()
            print("Looking up variable %s" % variable)

        if variable in self:
            return self[variable]
        elif self.parent:
            return self.parent.env_lookup(variable)
        else:
            raise EnvironmentError("Variable is unbound in the environment")

    def env_update(self, variable, value):
        if self.debug:
            self.env_display()
            print("Updating variable %s with value %s" % (variable, str(value)))

        if variable in self:
            self[variable] = value
        elif self.parent:
            self.parent.env_update(variable, value)
        else:
            raise EnvironmentError("Variable is unbound in the environment")

    def env_insert(self, variable, value):
        if self.debug:
            self.env_display()
            print("Inserting variable %s with value %s" % (variable, str(value)))

        if type(variable) != str:
            raise EnvironmentError("What are you doing?")

        if variable in self:
            raise EnvironmentError("Variable is already bound in this environment")
        else:
            self[variable] = value

    def env_extend(self, pairs):
        if self.debug:
            self.env_display()
            print("Extending environment with values %s" % str(pairs))

        return Environment(pairs, parent=self, debug=self.debug)
