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
        self.matching_indent = False
        self.matching_dedent = False
        self.matching_newline = False

        # pre-load the first couple tokens
        self.curr_token = self.lexer.lex()
        self.next_token = self.lexer.lex()
        #print("New parser")

    def match(self, token_type):
        print("Matching %s as %s" % (str(self.curr_token), str(token_type)))

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

        if self.curr_token is not None:
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

            # Is it indented as expected?
            if self.matching_indent:
                self.matching_indent = False
                if not self.indent(self.curr_token.col_no):
                    raise ParseError("Unexpected indention on line %d, "
                        "got %s expecting %d" % (
                            self.curr_token.line_no,
                            self.curr_token.col_no,
                            self.indent_level[-1])
                        )

            # Is it dedented as expected?
            elif self.matching_dedent:
                self.matching_dedent = False
                if not self.dedent(self.curr_token.col_no):
                    raise ParseError("Unexpected dedention on line %d, "
                            "got %s expecting %d" % (
                            self.curr_token.line_no,
                            self.curr_token.col_no,
                            self.indent_level[-1])
                            )

            # Is it on the same indention level as expected?
            elif self.matching_newline:
                self.matching_newline = False
                if not self.newline(self.curr_token.col_no):
                    raise ParseError("Incorrect indent on line %d, "
                            "got %s expecting %d" % (
                                self.curr_token.line_no,
                                self.curr_token.col_no,
                                self.indent_level[-1])
                            )

        # We just matched a terminator (newline), so be sure to match
        if token_type == Types.newline:
            self.matching_newline = True

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
        if x == self.indent_level[-1]:
            return True

        return False

    def start_nest(self):
        print("SNEST")
        self.match(Types.colon)
        self.match(Types.newline)
        self.matching_newline = False
        self.matching_indent = True

    def end_nest(self):
        print("ENEST", str(self.matching_newline))
        if not self.matching_newline:
            self.match(Types.newline)
        self.matching_newline = False
        self.matching_dedent = True

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
        print("NLP"+str(self.matching_indent)+str(self.matching_dedent)+str(self.matching_newline))
        return self.newline(self.curr_token.col_no)

    def formPending(self):
        return (self.exprPending() or self.defnPending())

    def form(self):
        if self.defnPending():
            self.defn()
        #elif self.exprPending():
        else:
            self.expr()

        if self.matching_newline:
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

