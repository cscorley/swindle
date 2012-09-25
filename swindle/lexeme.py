from swindle.types import Types

class Lexeme:
    def __init__(self, val, line_no, col_no, aux=0, unknown=False):
        if unknown:
            self.val_type = Types(None)
        else:
            self.val_type = Types(val)
        self.val = val
        self.line_no = line_no + 1
        self.col_no = col_no - len(str(val)) + 1
        self.aux = aux
        self.unknown = unknown

    def __str__(self):
        string = "(" + str(self.line_no)
        string += "," + str(self.col_no) + ")\t"
        string += str(self.val_type)
        if not (self.val_type.keyword or self.val_type.punctuation
                or self.val_type.whitespace):
            string += "\t" + str(self.val)
        if self.aux:
            string += "\taux=" + str(self.aux)
        if self.unknown:
            string += "\tUNKNOWN "
        return string
