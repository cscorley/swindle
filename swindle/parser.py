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
         return repr(self.message)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.curr_token = None
        self.next_token = None
        self.indent_level = [0] # a stack of the expected indentation levels.

        self.advance() # preload the first token

    def match(self, token_type, aux_pred=None, advance=True):
        if not self.check(token_type, aux_pred=aux_pred):
            if self.curr_token is None:
                pass # this is allowing for empty files
            #elif self.curr_token.val_type == Types.whitespace:
            elif token_type == Types.whitespace:
                raise ParseError(
"Unexpected indention level on line %d" % self.curr_token.line_no)
            else:
                raise ParseError(
"Unexpected token on line %d, column %d: expected %s, but got %s." %
(self.curr_token.line_no, self.curr_token.col_no, token_type, self.curr_token.val_type))

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
        if self.next_token:
            self.curr_token = self.next_token
            self.next_token = self.lexer.lex()
        else:
            self.curr_token = self.lexer.lex()
            self.next_token = self.lexer.lex()

#        if self.curr_token and self.curr_token.val_type == Types.unknown:
#            raise ParseError("What is this I don't even...")

    def program(self):
        self.form_list()

    def form_list(self):
        self.form()
        self.opt_form_list()

    def opt_form_list(self):
        if (self.newlinePending() and self.formPending(peek=True)):
            self.match(Types.whitespace, aux_pred=self.newline)
            self.form()
            self.opt_form_list()

    def newlinePending(self, peek=False):
        return self.check(Types.whitespace, aux_pred=self.newline, peek=peek)

    def formPending(self, peek=False):
        return (self.exprPending(peek=peek) or self.defnPending(peek=peek))

    def form(self):
        if self.defnPending():
            self.defn()
        else: #elif self.exprPending(): ?
            self.expr()

    def defn(self):
        self.match(Types.kw_def)
        self.variable()
        self.start_nest()
        self.expr()
        self.end_nest()

    def indent(self, x):
        if x > self.indent_level[-1]:
            self.indent_level.append(x)
            return True

        return False

    def dedent(self, x):
        while x < self.indent_level[-1]:
            self.indent_level.pop()

        if x == self.indent_level[-1]:
            return True

        return False

    def newline(self, x):
        if x == self.indent_level[-1]:
            return True

        return False


    def start_nest(self):
        self.match(Types.colon)
        self.match(Types.whitespace, aux_pred=self.indent)

    def end_nest(self):
        self.match(Types.whitespace, aux_pred=self.dedent)

    def variable(self):
        self.match(Types.variable)

    def expr(self):
        if self.literalPending():
            self.literal()
        elif self.proc_callPending():
            self.proc_call()
        elif self.variablePending():
            self.variable()
        elif self.if_exprPending():
            self.if_expr()
        elif self.lambda_exprPending():
            self.lambda_expr()
        elif self.set_exprPending():
            self.set_expr()
        #else:
        #    self.derived_expr()

    def derived_expr(self):
        pass
        # is this even needed here? aren't these derived expressions
        # just expressions that are defined by the environment?

    def literal(self):
        if self.booleanPending():
            self.match(Types.boolean)
        elif self.integerPending():
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
        if self.booleanPending():
            self.match(Types.boolean)
        elif self.integerPending():
            self.match(Types.integer)
        elif self.stringPending():
            self.match(Types.string)
        elif self.tuplePending():
            self.tuple()

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
        self.start_nest()
        #self.expr()
        self.form_list()
        self.end_nest()
        self.opt_elifs()
        self.opt_else()

    def opt_elifs(self):
        if self.elifPending():
            self.match(Types.kw_elif)
            self.match(Types.oparen)
            self.expr()
            self.match(Types.cparen)
            self.start_nest()
            #self.expr()
            self.form_list()
            self.end_nest()
            self.opt_elifs()

    def opt_else(self):
        if self.elsePending():
            self.match(Types.kw_else)
            self.start_nest()
            #self.expr()
            self.form_list()
            self.end_nest()

    def lambda_expr(self):
        self.match(Types.kw_lambda)
        self.parameters()
        self.start_nest()
        self.form_list()
        self.end_nest()

    def set_expr(self):
        self.match(Types.kw_set)
        self.variable()
        self.start_nest()
        self.expr()
        self.end_nest()

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
                self.proc_callPending(peek=peek)) # or
                # self.derived_exprPending())

    def literalPending(self, peek=False):
        return (self.booleanPending(peek=peek) or
                self.integerPending(peek=peek) or
                self.stringPending(peek=peek) or
                self.tuplePending(peek=peek) or
                self.quote_exprPending(peek=peek))

    def datumPending(self, peek=False):
        return (self.booleanPending(peek=peek) or
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

    def derived_exprPending(self, peek=False):
        # derp
        pass

    def booleanPending(self, peek=False):
        return self.check(Types.boolean, peek=peek)

    def integerPending(self, peek=False):
        return self.check(Types.integer, peek=peek)

    def stringPending(self, peek=False):
        return self.check(Types.string, peek=peek)

    def tuplePending(self, peek=False):
        return self.check(Types.obracket, peek=peek)

    def quote_exprPending(self, peek=False):
        return self.check(Types.quote, peek=peek)

