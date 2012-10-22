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
        self.indent_level = [0] # a stack of the expected indentation levels.

        self.advance() # preload the first token

    def match(self, token_type, aux_pred=None):
        if not self.check(token_type, aux_pred):
            if self.curr.val_type == Types.whitespace:
                raise ParseError(
"Unexpected indentation level on line %d" % self.curr.line_no)
            else:
                raise ParseError(
"Unexpected token on line %d, column %d: expected %s, but got %s." %
(self.curr.line_no, self.curr.col_no, token_type, self.curr.val_type))

        self.advance()

    def check(self, token_type, aux_pred=None):
        if aux_pred:
            return (self.curr.val_type == token_type
                and aux_pred(self.curr.aux))

        return (self.curr.val_type == token_type)

    def advance(self):
        self.curr = self.lexer.lex()

    def program(self):
        self.form_list()

    def form_list(self):
        self.form()
        self.match(Types.whitespace, aux_pred=self.newline)
        self.opt_form_list()

    def opt_form_list(self):
        if self.formPending():
            self.form()
            self.match(Types.whitespace, aux_pred=self.newline)
            self.opt_form_list()

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
        elif self.variablePending():
            self.variable()
            if self.proc_callPending():
                self.proc_call()
        elif self.if_exprPending():
            self.if_expr()
        elif self.lambda_exprPending():
            self.lambda_expr()
        elif self.set_exprPending():
            self.set_expr()
        else:
            self.derived_expr()

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

    def formPending(self):
        return (self.defnPending() or self.exprPending())

    def defnPending(self):
        return self.check(Types.kw_def)

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

    def datumPending(self):
        return (self.booleanPending() or
                self.integerPending() or
                self.stringPending() or
                self.tuplePending())

    def variablePending(self):
        return self.check(Types.variable)

    def if_exprPending(self):
        return self.check(Types.kw_if)

    def elifPending(self):
        return self.check(Types.kw_elif)

    def elsePending(self):
        return self.check(Types.kw_else)

    def lambda_exprPending(self):
        return self.check(Types.kw_lambda)

    def set_exprPending(self):
        return self.check(Types.kw_set)

    def proc_callPending(self):
        # cant use expr here without some sort of recursion :(
        return self.check(Types.oparen)

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
        return self.check(Types.obracket)

    def quote_exprPending(self):
        return self.check(Types.quote)

