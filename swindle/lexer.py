from swindle.lexeme import Lexeme
from io import BufferedReader

class Lexer:
    def __init__(self, fileptr):
        #self.fileptr = BufferedReader(fileptr)
        self.fileptr = fileptr
        self.line_count = 0
        self.indent_count = 0
        self.tokenize_whitespace = False
        self.whitespace_count = 0

    @property
    def indent_count(self):
        return self._indent_count

    @indent_count.setter
    def indent_count(self, val):
        if type(val) != int or val < 0:
            raise Exception("Indentation count must be a positive integer")

        self._indent_count = val

    def skip_whitespace(self):
        pass

    def getchar(self, f):
        # http://forums.devshed.com/python-programming-11/scan-a-text-file-one-character-at-a-time-522703.html
        for linenumber, line in enumerate(f):
            for columnnumber, char in enumerate(line):
                self.line_no = linenumber
                self.col_no = columnnumber
                yield char

    def lex(self):
        for c in self.getchar(self.fileptr):
            if self.tokenize_whitespace:
                if c == ' ':
                    self.whitespace_count += 1
                    continue
                else:
                    self.tokenize_whitespace = False
                    yield Lexeme(' ', aux=self.whitespace_count)

            if (   c == '('
                or c == ')'
                or c == ':'
                or c == '`'
                or c == '['
                or c == ']'
                or c == '+'  # may need to pass these off to lex_number
                or c == '-'):
                yield Lexeme(c)
            elif c.isdigit():
                yield self.lex_number(c)
            elif c.isalpha():
                yield self.lex_id_or_keyword(c)
            elif c == '"':
                yield self.lex_string(c)
            elif c == '\n':
                # begin tokenizing whitespace for indent
                self.tokenize_whitespace = True
                self.whitespace_count = 0
                continue
            else:
                yield Lexeme(c, unknown=True)

    def lex_number(self,c):
        return Lexeme(c)

    def lex_id_or_keyword(self,c):
        return Lexeme(c)

    def lex_string(self,c):
        return Lexeme(c)
