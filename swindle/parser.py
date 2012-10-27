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

        # magic flags
        self.newline_seen = False

        # pre-load the first couple tokens
        self.curr_token = self.lexer.lex()
        self.next_token = self.lexer.lex()

    def match(self, token_type):
        #print("Matching %s as %s" % (str(self.curr_token), str(token_type)))

        # Handle special cases for no token and lexer progress.
        if (self.curr_token is None
            and not self.lexer.done):
            raise ParseError("No token received from lexer when lexer wasn't finished.")
        # Allow for the last newline to go unmatched if we are EOF.
        # May be a better way to do this, like... creating a EOF token.
        elif (self.curr_token is None
                and self.lexer.done
                and not token_type == Types.newline):
            raise ParseError("Found EOF when expecting token %s" % token_type)

        # We can't even do anything if we try to match on an unknown.
        if self.check(Types.unknown):
            raise ParseError("Unknown token found.")

        # Make sure the token is the right one
        if not self.check(token_type):
            raise ParseError("Unexpected token on line %d, column %d: "
                "expected %s, but got %s with val='%s' and aux=%s." % (
                    self.curr_token.line_no,
                    self.curr_token.col_no,
                    token_type,
                    self.curr_token.val_type,
                    self.curr_token.val,
                    self.curr_token.aux)
                )

        # We just matched a terminator (newline), so be sure to match
        if token_type == Types.newline:
            self.newline_seen = True
        else:
            self.newline_seen = False

        self.advance()


    def check(self, token_type, peek=False):
        if peek:
            token = self.next_token
        else:
            token = self.curr_token

        if token:
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
        #print("N %d %d" % (x, self.indent_level[-1]))
        if x == self.indent_level[-1]:
            return True

        return False

    def start_nest(self):
        self.match(Types.colon)
        self.match(Types.newline)
        if self.curr_token and not self.indent(self.curr_token.col_no):
            raise ParseError("Unexpected indention level on line %d, "
                "got %s expecting %d" % (
                    self.curr_token.line_no,
                    self.curr_token.col_no,
                    self.indent_level[-1])
                )

    def end_nest(self):
        if self.curr_token and not self.dedent(self.curr_token.col_no):
            raise ParseError("Unexpected indention level on line %d, "
                "got %s expecting %d" % (
                    self.curr_token.line_no,
                    self.curr_token.col_no,
                    self.indent_level[-1])
                )

    def program(self):
        self.opt_form_list()

    def form_list(self):
        self.form()
        self.opt_form_list()

    def form_block(self):
        self.start_nest()
        self.form_list()
        self.end_nest()

    def opt_form_list(self):
        if self.formPending() and self.newlinePending():
            self.form()
            self.opt_form_list()

    def newlinePending(self):
        val = self.newline(self.curr_token.col_no)
        #print("NLP "+str(val)+" "+str(self.newline_seen))
        return val

    def formPending(self):
        val = (self.exprPending() or self.defnPending())
        #print("FORM %s %s" % (str(val), str(self.curr_token)))
        return val

    def form(self):
        if self.defnPending():
            self.defn()
        #elif self.exprPending():
        else:
            self.expr()

        #print("FORMEND"+" "+str(self.newline_seen))
        if not self.newline_seen:
            self.match(Types.newline)

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
        self.opt_datum_list()
        self.match(Types.cbracket)

    def opt_datum_list(self):
        if self.datumPending():
            self.datum()
            self.opt_datum_list()

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
        if self.parametersPending():
            self.parameters()
        self.form_block()

    def set_expr(self):
        self.match(Types.kw_set)
        self.variable()
        self.form_block()

    def proc_call(self):
        self.match(Types.variable)
        self.match(Types.oparen)
        self.opt_expr_list()
        self.match(Types.cparen)

    def opt_expr_list(self):
        if self.exprPending():
            self.expr()
            self.opt_expr_list()

    def parameters(self):
        self.match(Types.oparen)
        self.variable()
        self.opt_variable_list()
        self.match(Types.cparen)

    def opt_variable_list(self):
        if self.variablePending():
            self.variable()
            self.opt_variable_list()

    def parametersPending(self):
        return self.check(Types.oparen)

    def defnPending(self):
        return self.check(Types.kw_def)

    def exprPending(self):
        return (self.literalPending() or
                self.variablePending() or
                self.if_exprPending() or
                self.lambda_exprPending() or
                self.set_exprPending() or
                self.proc_callPending())

    def literalPending(self):
        return (
                self.integerPending() or
                self.stringPending() or
                self.tuplePending() or
                self.quote_exprPending())

    def datumPending(self):
        return (
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
        return (self.check(Types.variable) and self.check(Types.oparen, peek=True))

    def integerPending(self):
        return self.check(Types.integer)

    def stringPending(self):
        return self.check(Types.string)

    def tuplePending(self):
        return self.check(Types.obracket)

    def quote_exprPending(self):
        return self.check(Types.quote)

