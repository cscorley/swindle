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

        # For building parse trees
        self.left = None
        self.right = None

    def __str__(self):
        string = "(" + str(self.line_no)
        string += "," + str(self.col_no) + ")\t"
        string += str(self.val_type)
        string += "\t" + str(self.val)
        if self.aux:
            string += "\taux=" + str(self.aux)
        return string

    @property
    def left(self):
        return self._left_lexeme

    @left.setter
    def left(self, val):
        if type(val) is Lexeme or val is None:
            self._left_lexeme = val
        else:
            raise Exception("Left lexeme is not a Lexeme object")

    @property
    def right(self):
        return self._right_lexeme

    @right.setter
    def right(self, val):
        if type(val) is Lexeme or val is None:
            self._right_lexeme = val
        else:
            raise Exception("Right lexeme is not Lexeme object")
