# types.py
#
# Still needs to be refactored so that each keyword and punctuation has
# it's own type.
#
# author: Christopher S. Corley

KEYWORDS = frozenset(["def",
                    "lambda",
                    "set!",
                    "if",
                    "elif",
                    "else",
                    "True",
                    "False"
                    ])
PUNCTUATION = frozenset(":()")
LITERALS_PUNC = frozenset("[]+-`")

class Enum(set):
    # http://stackoverflow.com/a/2182437
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

Types = Enum(['keyword', 'punctuation', 'literals_punc', 'whitespace',
        'boolean', 'integer', 'string', 'variable', 'unknown'])

def get_type(val):
    if val is None:
        return Types.unknown
    elif val in KEYWORDS:
        if val == "True" or val == "False":
            return Types.boolean
        else:
            return Types.keyword
    elif val in PUNCTUATION:
        return Types.punctuation
    elif val in LITERALS_PUNC:
        return Types.literals_punc
    else:
        if val.isdigit():
            return Types.integer
        elif val == " ":
            return Types.whitespace
        elif val.startswith('"'):
            return Types.string
        else:
            return Types.variable


