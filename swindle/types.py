# types.py
#
# author: Christopher S. Corley

KEYWORDS = frozenset(["def",
                    "lambda",
                    "set!",
                    "if",
                    "elif",
                    "else"
                    ])
PUNCTUATION = frozenset(":()")
LITERALS_PUNC = frozenset("[]+-`")

class Enum(set):
    # http://stackoverflow.com/a/2182437
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

Types = Enum([
    'kw_def', 'kw_lambda', 'kw_set', 'kw_if', 'kw_elif', 'kw_else',
    'colon', 'oparen', 'cparen',
    'obracket', 'cbracket', 'plus', 'minus', 'quote',
    'whitespace', 'newline',
    'integer', 'string', 'variable',
    'unknown'])

def get_type(val):
    if val is None:
        return Types.unknown
    elif val == 'def':
        return Types.kw_def
    elif val == 'lambda':
        return Types.kw_lambda
    elif val == 'set!':
        return Types.kw_set
    elif val == 'if':
        return Types.kw_if
    elif val == 'elif':
        return Types.kw_elif
    elif val == 'else':
        return Types.kw_else
    elif val == ':':
        return Types.colon
    elif val == '(':
        return Types.oparen
    elif val == ')':
        return Types.cparen
    elif val == '[':
        return Types.obracket
    elif val == ']':
        return Types.cbracket
    elif val == '+':
        return Types.plus
    elif val == '-':
        return Types.minus
    elif val == '`':
        return Types.quote
    elif val == " ":
        return Types.whitespace
    elif val == "\n":
        return Types.newline
    elif val.isdigit():
        return Types.integer
    elif val.startswith('"'):
        return Types.string
    else:
        return Types.variable


