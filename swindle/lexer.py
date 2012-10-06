# lexer.py
#
# author: Christopher S. Corley

from swindle.lexeme import Lexeme
from swindle.types import get_type
from swindle.types import Types
from io import TextIOWrapper

class Lexer:
    def __init__(self, fileptr):
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
            self.make_error("Indentation count must be a positive integer")

        self._indent_count = val

    @property
    def line_no(self):
        return self._line_no

    @line_no.setter
    def line_no(self, val):
        self._line_no = val + 1

    @property
    def col_no(self):
        return self._col_no

    @col_no.setter
    def col_no(self, val):
        self._col_no = val + 1

    def make_error(self, msg):
        if type(self.fileptr) is TextIOWrapper:
            exception_str = str(self.fileptr.name) + "\n"
        else:
            exception_str = str(type(self.fileptr)) + "\n\t"
            exception_str += str(self.fileptr) + "\n"

        exception_str += "Error on line " + str(self.line_no)
        exception_str += ", character " +  str(self.col_no)
        exception_str += ": \n\t" + str(msg)

        raise Exception(exception_str)


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
                        # not sure why this else was there, it breaks comment mode!
#                    else:
#                        return None

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

        if (get_type(c) is not Types.punctuation
            and get_type(c) is not Types.whitespace
            and c != '\n'):
            self.make_error("Variable names must begin with a letter.")

        self.saved_char = c
        return Lexeme(cstr, self.line_no, self.col_no)

    def lex_id_or_keyword(self):
        cstr = self.get_next_char()
        c = self.get_next_char()
        while c and (c.isalpha()
                  or c.isdigit()
                  or c == "_"
                  or c == "!"):
            cstr += c
            c = self.get_next_char()

        if c and (get_type(c) is not Types.punctuation
            and get_type(c) is not Types.whitespace
            and c != '\n'):
            self.make_error("Variable names cannot contain character " + c)

        self.saved_char = c
        return Lexeme(cstr, self.line_no, self.col_no)


    def lex_string(self):
        cstr = self.get_next_char() # if we want to collect beginning "
#        cstr = str()
        c = self.get_next_char()
        while c:
            if c == '\\':
                cstr += c
                c = self.get_next_char()
            elif c == '"':
                cstr += c # if we want to collect ending "
                return Lexeme(cstr, self.line_no, self.col_no)

            cstr += c
            c = self.get_next_char()
