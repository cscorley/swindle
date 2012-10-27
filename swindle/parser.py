# scanner.py
#
# author: Christopher S. Corley

import os
import sys
from swindle.types import Types

class ParseError(Exception):
     def __init__(self, value):
         self.message = value
     def __str__(self):
         return str(self.message)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.indent_level = [1] # a stack of the expected indentation levels.
        self.matching_indent = False
        self.matching_dedent = False
        self.matching_newline = False

        self.curr_token = self.lexer.lex()
        self.next_token = self.lexer.lex()
        print("New parser")

    def match(self, token_type, aux_pred=None, advance=True):
        if self.curr_token is None and not self.lexer.done:
            raise ParseError("Your life. It's over.")

        if self.lexer.done and token_type:
            raise ParseError("Found EOF when expecting token %s" % token_type)

        if self.check(Types.unknown):
            raise ParseError("Unknown token found.")

        if not self.check(token_type, aux_pred=aux_pred) and self.curr_token:
            raise ParseError(
"Unexpected token on line %d, column %d: expected %s, but got %s with val='%s' and aux=%s." %
(self.curr_token.line_no, self.curr_token.col_no, token_type,
    self.curr_token.val_type, self.curr_token.val, self.curr_token.aux))

        if self.matching_indent and self.curr_token:
            self.matching_indent = False
            if not self.indent(self.curr_token.col_no):
                raise ParseError(
"Unexpected INdention level on line %d, got %s expecting %d" % (self.curr_token.line_no,
                self.curr_token.col_no, self.indent_level[-1]))
        if self.matching_dedent and self.curr_token:
            self.matching_dedent = False
            if not self.dedent(self.curr_token.col_no):
                raise ParseError(
"Unexpected DEdention level on line %d, got %s expecting %d" % (self.curr_token.line_no,
                self.curr_token.col_no, self.indent_level[-1]))
        if self.matching_newline and self.curr_token:
            self.matching_newline = False
            if not self.newline(self.curr_token.col_no):
                raise ParseError(
"Unexpected newline level on line %d, got %s expecting %d" % (self.curr_token.line_no,
                self.curr_token.col_no, self.indent_level[-1]))

        if token_type == Types.newline:
            self.matching_newline = True

        print("Matched %s as %s" % (str(self.curr_token), str(token_type)))

        if advance:
            self.advance()


    def check(self, token_type, aux_pred=None, peek=False):
        if peek:
            token = self.next_token
        else:
            token = self.curr_token

        if token:
            if aux_pred:
                return (token.val_type == token_type
                    and aux_pred(token.aux))


            return (token.val_type == token_type)

        return False

    def advance(self):
        if self.next_token is not None:
            self.curr_token = self.next_token
            self.next_token = self.lexer.lex()
        else:
            self.curr_token = self.lexer.lex()
            self.next_token = self.lexer.lex()

    def indent(self, x):
        if x > self.indent_level[-1]:
            self.indent_level.append(x)
            return True

        return False

    def dedent(self, x):
        if x < self.indent_level[-1]:
            self.indent_level.pop()
            return True

        return False

    def newline(self, x):
        if x == self.indent_level[-1]:
            return True

        return False

    def start_nest(self):
        self.match(Types.colon)
        self.match(Types.newline)
        self.matching_newline = False
        self.matching_indent = True

    def end_nest(self):
        if not self.matching_newline:
            self.match(Types.newline)
        self.matching_dedent = True

    def program(self):
        if self.formPending():
            self.form_list()

    def form_list(self):
        self.form()
        self.opt_form_list()

    def form_block(self):
        self.start_nest()
        self.form_list()
        self.end_nest()

    def opt_form_list(self):
        #if (self.newlinePending() and self.formPending(peek=True)):
        if self.formPending():# and self.newlinePending(peek=True):
            self.form()
            self.match(Types.newline)
            self.opt_form_list()

    def newlinePending(self, peek=False):
        return self.check(Types.newline, peek=peek)

    def formPending(self, peek=False):
        if peek and self.next_token:
            return (self.newline(self.next_token.col_no) and
            (self.exprPending(peek=peek) or self.defnPending(peek=peek)))
        elif self.curr_token:
            return (self.newline(self.curr_token.col_no) and
            (self.exprPending(peek=peek) or self.defnPending(peek=peek)))

        return False

    def form(self):
        if self.defnPending():
            self.defn()
        elif self.exprPending():
        #else:
            self.expr()

    def defn(self):
        self.match(Types.kw_def)
        self.variable()
        self.form_block()

    def variable(self):
        self.match(Types.variable)

    def expr(self):
        if self.proc_callPending():
            self.proc_call()
        elif self.if_exprPending():
            self.if_expr()
        elif self.lambda_exprPending():
            self.lambda_expr()
        elif self.set_exprPending():
            self.set_expr()
        elif self.literalPending():
            self.literal()
        else:
            self.variable()

    def literal(self):
        if self.integerPending():
            self.match(Types.integer)
        elif self.stringPending():
            self.match(Types.string)
        elif self.tuplePending():
            self.tuple()
        else:
            self.quote_expr()

    def quote_expr(self):
        self.match(Types.quote)
        self.datum()

    def datum(self):
        if self.integerPending():
            self.match(Types.integer)
        elif self.stringPending():
            self.match(Types.string)
        elif self.tuplePending():
            self.tuple()
        else:
            # for symbols?
            self.variable()

    def tuple(self):
        self.match(Types.obracket)
        self.datum()
        self.opt_datum_list()
        self.match(Types.cbracket)

    def if_expr(self):
        self.match(Types.kw_if)
        self.match(Types.oparen)
        self.expr()
        self.match(Types.cparen)
        self.form_block()
        self.opt_elifs()
        self.opt_else()


    def opt_elifs(self):
        if self.elifPending():
            self.match(Types.kw_elif)
            self.match(Types.oparen)
            self.expr()
            self.match(Types.cparen)
            self.form_block()
            self.opt_elifs()

    def opt_else(self):
        if self.elsePending():
            self.match(Types.kw_else)
            self.form_block()

    def lambda_expr(self):
        self.match(Types.kw_lambda)
        self.parameters()
        self.form_block()

    def set_expr(self):
        self.match(Types.kw_set)
        self.variable()
        self.form_block()

    def proc_call(self):
#        self.expr()
        self.match(Types.variable)
        self.match(Types.oparen)
        self.opt_expr_list()
        self.match(Types.cparen)

    def opt_expr_list(self):
        if self.exprPending():
            self.expr()
            self.opt_expr_list()

    def parameters(self):
        if self.check(Types.oparen):
            self.match(Types.oparen)
            self.variable()
            self.opt_variable_list()
            self.match(Types.cparen)

    def opt_variable_list(self):
        if self.variablePending():
            self.variable()
            self.opt_variable_list()

    def defnPending(self, peek=False):
        return self.check(Types.kw_def, peek=peek)

    def exprPending(self, peek=False):
        return (self.literalPending(peek=peek) or
                self.variablePending(peek=peek) or
                self.if_exprPending(peek=peek) or
                self.lambda_exprPending(peek=peek) or
                self.set_exprPending(peek=peek) or
                self.proc_callPending(peek=peek))

    def literalPending(self, peek=False):
        return (
                self.integerPending(peek=peek) or
                self.stringPending(peek=peek) or
                self.tuplePending(peek=peek) or
                self.quote_exprPending(peek=peek))

    def datumPending(self, peek=False):
        return (
                self.integerPending(peek=peek) or
                self.stringPending(peek=peek) or
                self.tuplePending(peek=peek))

    def variablePending(self, peek=False):
        return self.check(Types.variable, peek=peek)

    def if_exprPending(self, peek=False):
        return self.check(Types.kw_if, peek=peek)

    def elifPending(self, peek=False):
        return self.check(Types.kw_elif, peek=peek)

    def elsePending(self, peek=False):
        return self.check(Types.kw_else, peek=peek)

    def lambda_exprPending(self, peek=False):
        return self.check(Types.kw_lambda, peek=peek)

    def set_exprPending(self, peek=False):
        return self.check(Types.kw_set, peek=peek)

    def proc_callPending(self, peek=False):
        # cant use expr here without some sort of recursion :(
        return (self.check(Types.variable, peek=peek) and self.check(Types.oparen, peek=True))

    def integerPending(self, peek=False):
        return self.check(Types.integer, peek=peek)

    def stringPending(self, peek=False):
        return self.check(Types.string, peek=peek)

    def tuplePending(self, peek=False):
        return self.check(Types.obracket, peek=peek)

    def quote_exprPending(self, peek=False):
        return self.check(Types.quote, peek=peek)

