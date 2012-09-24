
class Lexeme:
    def __init__(self, val, aux=0, unknown=False):
        self.unknown = unknown
        self.val = val
        self.aux = aux

    def __str__(self):
        return str(self.val) + ", " + str(self.aux)
