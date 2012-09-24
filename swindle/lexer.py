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
        self.comment_mode = False
        self.saved_char = None

        self.character = self.char_generator()

    @property
    def indent_count(self):
        return self._indent_count

    @indent_count.setter
    def indent_count(self, val):
        if type(val) != int or val < 0:
            raise Exception("Indentation count must be a positive integer")

        self._indent_count = val

    def char_generator(self):
        for self.line_no, line in enumerate(self.fileptr):
            for self.col_no, char in enumerate(line):
                self.saved_char = None
                yield char

    def get_next_char(self):
        if self.saved_char:
            c = self.saved_char
            self.saved_char = None
        else:
            try:
                c = next(self.character)
            except StopIteration:
                return None

        return c

    def skip_whitespace(self):
        c = self.get_next_char()
        while c:
            if self.tokenize_whitespace:
                if c == ' ':
                    self.whitespace_count += 1
                    c = self.get_next_char()
                    continue
                elif c == '\n':
                    # handle empty lines
                    c = self.get_next_char()
                    continue
                else:
                    self.tokenize_whitespace = False
                    self.saved_char = c
                    if self.whitespace_count > 0:
                        return Lexeme(' ',
                                self.line_no,
                                self.col_no,
                                aux=self.whitespace_count)
                    else:
                        return None

            if self.comment_mode:
                if c == '\n':
                    self.comment_mode = False
            elif c == '#':
                self.comment_mode = True
            elif c == ' ':
                c = self.get_next_char()
                continue
            elif c == '\n':
                # begin tokenizing whitespace for indent
                self.comment_mode = False
                self.tokenize_whitespace = True
                self.whitespace_count = 0
            else:
                self.saved_char = c
                return None

            c = self.get_next_char()

        return None

    def lex(self):
        ws_token = self.skip_whitespace()
        if ws_token:
            return ws_token

        c = self.get_next_char()
        if c:
            if (   c == '('
                or c == ')'
                or c == ':'
                or c == '`'
                or c == '['
                or c == ']'
                or c == '+'  # may need to pass these off to lex_number
                or c == '-'):
                return Lexeme(c, self.line_no, self.col_no)
            elif c.isdigit():
                self.saved_char = c
                return self.lex_number()
            elif c.isalpha():
                self.saved_char = c
                return self.lex_id_or_keyword()
            elif c == '"':
                self.saved_char = c
                return self.lex_string()
            else:
                return Lexeme(c,
                        self.line_no,
                        self.col_no,
                        unknown=True)

        return None

    def lex_number(self):
        cstr = self.get_next_char()
        c = self.get_next_char()
        while c.isdigit():
            cstr += c
            c = self.get_next_char()

        self.saved_char = c
        return Lexeme(cstr, self.line_no, self.col_no)

    def lex_id_or_keyword(self):
        cstr = self.get_next_char()
        c = self.get_next_char()
        while (c.isalpha()
                or c.isdigit()
                or c == "_"
                or c == "!"):
            cstr += c
            c = self.get_next_char()

        self.saved_char = c
        return Lexeme(cstr, self.line_no, self.col_no)


    def lex_string(self):
        cstr = self.get_next_char()
        c = self.get_next_char()
        while c:
            if c == '\\':
                cstr += c
            elif c != '"':
                break

            cstr += c
            c = self.get_next_char()

        self.saved_char = c
        return Lexeme(cstr, self.line_no, self.col_no)
