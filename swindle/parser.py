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
        self.curr = None
        self.indent = [0] # a stack of the expected indentation levels.

    def match(self, token_type, aux_pred=None):
        if not check(token_type, aux_pred):
            if token_type == Types.whitespace:
                raise ParseError(
"Unexpected indentation level on line %d" % self.curr.line_no)
            else:
                raise ParseError(
"Unexpected token on line %d, column %d: expected %s, but got %s." %
(self.curr.line_no, self.curr.col_no, token_type, self.curr.val_type))

    def check(self, token_type, aux_pred=None):
        return (self.curr.val_type == token_type
                and aux_pred(self.curr.aux))

    def advance(self):
        self.curr = self.lexer.lex()

    def program(self):
        self.form_list()

    def form_list(self):
        self.form()
        self.opt_form_list()

    def opt_form_list(self):
        if self.formPending():
            self.form()
            self.opt_form_list()

    def form(self):
        if self.defnPending():
            self.defn()
        else: #elif self.exprPending(): ?
            self.expr()


    def defn(self):
        self.match(Types.def)
        self.variable()
        self.start_nest()
        self.expr()
        self.end_nest()

    def start_nest(self):
        self.match(Types.colon)
        self.match(Types.whitespace, aux_pred=lambda x: x > self.ident[-1])

    def end_nest(self):
        self.match(Types.whitespace, aux_pred=lambda x: x == self.ident[-1])
        # matching several dedents in this way is not going to work here.

    def variable(self):
        self.match(Types.variable)

    def expr(self):
        if self.literalPending():
            self.literal()
        elif self.variablePending():
            self.variable()
        elif self.if_exprPending():
            self.if_expr()
        elif self.lambda_exprPending():
            self.lambda_expr()
        elif self.set_exprPending():
            self.set_expr()
        elif self.proc_callPending():
            self.proc_call()
        else:
            self.derived_expr()

    def literal(self):
        elif self.booleanPending():
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

    def if_expr(self):
        self.match(Types.if)
        self.match(Types.oparen)
        self.expr()
        self.match(Types.cparen)
        self.start_nest()
        self.expr()
        self.end_nest()
        self.opt_elifs()
        self.opt_else()

    def opt_elifs(self):
        if self.elifPending():
            self.match(Type.elif)
            self.match(Types.oparen)
            self.expr()
            self.match(Types.cparen)
            self.start_nest()
            self.expr()
            self.end_nest()
            self.opt_elifs()

    def opt_else(self):
        if self.elsePending():
            self.match(Type.else)
            self.start_nest()
            self.expr()
            self.end_nest()

    def lambda_expr(self):
        self.match(Types.lambda)
        self.parameters()
        self.start_nest()
        self.form_list()
        self.end_nest()

    def set_expr(self):
        self.match(Types.set)
        self.variable()
        self.start_nest()
        self.expr()
        self.end_nest()

    def proc_call(self):
        self.expr()
        self.match(Types.oparen)
        self.opt_expr_list()
        self.match(Types.cparen)

    def opt_expr_list(self):
        if self.exprPending():
            self.expr()
            self.opt_expr_list()

    def parameters(self):
        if self.check(Type.oparen):
            self.match(Type.oparen)
            self.variable()
            self.opt_variable_list()

    def opt_variable_list(self):
        if self.variablePending():
            self.variable()
            self.opt_variable_list()

    def formPending(self):
        return (self.defnPending() or self.exprPending())

    def defnPending(self):
        return self.check(Types.def)

    def exprPending(self):
        return (self.literalPending() or
                self.variablePending() or
                self.if_exprPending() or
                self.lambda_exprPending() or
                self.set_exprPending() or
                self.proc_callPending() or
                self.derived_exprPending())

    def literalPending(self):
        return (self.booleanPending() or
                self.integerPending() or
                self.stringPending() or
                self.tuplePending() or
                self.quote_exprPending())


    def variablePending(self):
        return self.check(Types.variable)

    def if_exprPending(self):
        return self.check(Types.if)

    def elifPending(self):
        return self.check(Types.elif)

    def elsePending(self):
        return self.check(Types.else)

    def lambda_exprPending(self):
        return self.check(Types.lambda)

    def set_exprPending(self):
        return self.check(Types.set)

    def proc_callPending(self):
        # derp
        pass

    def derived_exprPending(self):
        # derp
        pass

    def booleanPending(self):
        return self.check(Types.boolean)

    def integerPending(self):
        return self.check(Types.integer)

    def stringPending(self):
        return self.check(Types.string)

    def tuplePending(self):
        return self.check(Types.tuple)

    def quote_exprPending(self):
        return self.check(Types.quote)

