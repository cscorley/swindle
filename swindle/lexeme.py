from swindle.types import get_type as get_type
from swindle.types import Types as Types

class Lexeme:
    def __init__(self, val, line_no, col_no, aux=0, unknown=False):
        if unknown:
            self.val_type = get_type(None)
        else:
            self.val_type = get_type(val)
        self.val = val
        self.line_no = line_no
        self.col_no = col_no - len(str(val))
        self.aux = aux
        self.unknown = unknown

    def __str__(self):
        string = "(" + str(self.line_no)
        string += "," + str(self.col_no) + ")\t"
        string += str(self.val_type)
        string += "\t" + str(self.val)
        if self.aux:
            string += "\taux=" + str(self.aux)
        return string
