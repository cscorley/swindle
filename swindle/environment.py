# environment.py
#
# author: Christopher S. Corley


class Environment:
    def __init__(self, debug=False):
        self.debug = debug
        if self.debug:
            print("Creating a new environment")
        pass
