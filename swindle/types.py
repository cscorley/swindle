# keywords
KEYWORDS = frozenset(["def",
                    "lambda",
                    "set!",
                    "if",
                    "else",
                    "True",
                    "False"
                    ])
# punctuation
PUNCTUATION = frozenset(":[]()+-`")

# variables
# operators
# numbers


class Types:
    def __init__(self, val):
        self.keyword = False
        self.punctuation = False
        self.whitespace = False
        self.string = False
        self.integer = False
        self.variable = False

        if val in KEYWORDS:
            self.keyword = True
            self.type_string = val
        elif val in PUNCTUATION:
            self.punctuation = True
            self.type_string = val
        else:
            if val.isdigit():
                self.integer = True
                self.type_string = "int"
            if val == " ":
                self.whitespace = True
                self.type_string = "ws"
            else:
                self.variable = True
                self.type_string = "var"

    def __str__(self):
        return str(self.type_string)
