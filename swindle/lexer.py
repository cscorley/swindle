# lexer.py
#
# author: Christopher S. Corley

from swindle.lexeme import Lexeme
from swindle.types import (Types, get_type, PUNCTUATION)
from io import TextIOWrapper

class Lexer:
    def __init__(self, fileptr):
        # fileptr is generally a TextIOWrapper when reading from a file
        self.fileptr = fileptr

        self.tokenize_whitespace = False # like python, we tokenize all whitespace
        self.whitespace_count = 0
        self.comment_mode = False

        # To emulate pushing things back to the stream
        self.saved_char = None

        # character is a generator so we can have nice reading things
        # like next(self.character)
        self.character = self.char_generator()

    # line_no and col_no have special properties because we always want
    # line 0 to be line 1.
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


    # a convenient way to count line numbers and read things character
    # by character.
    def char_generator(self):
        for self.line_no, line in enumerate(self.fileptr):
            for self.col_no, char in enumerate(line):
                self.saved_char = None
                yield char

    # returning None will represent an EOF marker, but also make looping
    # easy since loops stop on None or False
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
        # skip_whitespace will do just that, but in swindle we need the
        # extra property of tokenizing the whitespace at the beginning
        # of a line as well. So, this will either return a whitespace
        # Lexeme or None.
        c = self.get_next_char()
        while c:
            if self.tokenize_whitespace:
                if c == ' ':
                    self.whitespace_count += 1
                else:
                    self.tokenize_whitespace = False
                    self.saved_char = c
                    return Lexeme(' ',
                            self.line_no,
                            self.col_no,
                            aux=self.whitespace_count)
            else:
                if self.comment_mode:
                    if c == '\n':
                        self.comment_mode = False
                        self.tokenize_whitespace = True
                        self.whitespace_count = 0
                        return Lexeme(c,
                                self.line_no,
                                self.col_no)
                elif c == '#':
                    self.comment_mode = True
                elif c == ' ':
                    pass
                elif c == '\n':
                    # begin tokenizing whitespace for indent
                    self.comment_mode = False
#                    self.tokenize_whitespace = True
                    self.whitespace_count = 0
                    return Lexeme(c,
                            self.line_no,
                            self.col_no)
                else:
                    self.saved_char = c
                    return None

            c = self.get_next_char()

        return None

    # Will return None if there are no characters left.
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
                or c == ']'):
#                or c == '+'  # may need to pass these off to lex_number
#                or c == '-'):
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

        if (c not in PUNCTUATION
            and c != ' '
            and c != '\n'):
            self.make_error("Variable names must begin with a letter.")

        self.saved_char = c
        return Lexeme(cstr, self.line_no, self.col_no)

    def lex_id_or_keyword(self):
        # we already know the saved_char contains the first letter of
        # the id or keyword, so get it back off again.
        cstr = self.get_next_char()
        c = self.get_next_char()
        while c and (c.isalpha()
                  or c.isdigit()
                  or c == "_"
                  # for the set! keyword
                  or c == "!"):
            cstr += c
            c = self.get_next_char()

        if c and (c not in PUNCTUATION
            and c != ' '
            and c != '\n'):
            self.make_error("Variable names cannot contain character " + c)

        self.saved_char = c
        return Lexeme(cstr, self.line_no, self.col_no)


    def lex_string(self):
        cstr = self.get_next_char() # if we want to collect beginning "
        # which we do, because we want to have an easy way for Lexeme
        # to detect the string literal
        c = self.get_next_char()
        while c:
            if c == '\\':
                # this will allow us to grab any escaped character
                cstr += c
                c = self.get_next_char()
            elif c == '"':
                cstr += c # if we want to collect ending "
                return Lexeme(cstr, self.line_no, self.col_no)

            cstr += c
            c = self.get_next_char()
