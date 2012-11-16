# lexeme.py
#
# author: Christopher S. Corley

from swindle.types import get_type
from swindle.types import Types

class Lexeme:
    def __init__(self, val, line_no, col_no, token_type=None, aux=None, unknown=False):
        if unknown:
            self.val_type = get_type(None)
        elif token_type:
            self.val_type = token_type
        else:
            self.val_type = get_type(val)
        self.unknown = unknown

        # holds the tokenized string
        self.val = val
        self.line_no = line_no
        self.col_no = col_no - len(str(val))

        # extra stuff, mostly just used for whitespace
        self.aux = aux

        # For building parse trees
        self.left = None
        self.right = None

    def __str__(self):
        string = "{"
        string += "(" + str(self.line_no)
        string += "," + str(self.col_no) + ")\t"
        string += str(self.val_type)
        if not self.val == '\n':
            string += "\t" + str(self.val)
        if self.aux is not None:
            string += "\taux=" + str(self.aux)

        if self.left or self.right:
            string += "\n\t<< " + str(self.left)
            string += "\n\t>> " + str(self.right)

        string += "}\n"

        return string

    # Make self.left and self.right special properties so we can do some
    # checking on the values before the assignment is made
    @property
    def left(self):
        return self._left_lexeme

    @left.setter
    def left(self, val):
        if type(val) is Lexeme or val is None:
            if val is self:
                raise Exception("Lexeme cannot have self as a child")

            self._left_lexeme = val
        else:
            raise Exception("Left lexeme is not a Lexeme object")

    @property
    def right(self):
        return self._right_lexeme

    @right.setter
    def right(self, val):
        if type(val) is Lexeme or val is None:
            if val is self:
                raise Exception("Lexeme cannot have self as a child")

            self._right_lexeme = val
        else:
            raise Exception("Right lexeme is not Lexeme object")
