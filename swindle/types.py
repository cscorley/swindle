
class Types:
    def __init__(self, val):
        # keywords
        keywords = frozenset(["def",
                            "lambda",
                            "set!",
                            "if",
                            "else",
                            "True",
                            "False"
                            ])
        # punctuation
        punctuation = frozenset(":[]()+-`")

        # variables
        # operators
        # numbers

        if val in keywords:
            self.type_string = val
        elif val in punctuation:
            self.type_string = val
        else:
            if val.isdigit():
                self.type_string = "int"
            if val == " ":
                self.type_string = "ws"
            else:
                self.type_string = "var"

    def __str__(self):
        return str(self.type_string)
