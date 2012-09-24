from swindle.types import Types

class Lexeme:
    def __init__(self, val, line_no, col_no, aux=0, unknown=False):
        self.val_type = Types(val)
        self.val = val
        self.line_no = line_no
        self.col_no = col_no
        self.aux = aux
        self.unknown = unknown

    def __str__(self):
        string = "(" + str(self.line_no)
        string += "," + str(self.col_no) + ")\t"
        string += str(self.val_type) + "\t"
        string += str(self.val)
        if self.aux:
            string += ", " + str(self.aux)
        if self.unknown:
            string += ", " + str(self.unknown)
        return string
