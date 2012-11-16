# scanner.py
#
# author: Christopher S. Corley

import os
import sys
from swindle.types import Types
from swindle.lexeme import Lexeme

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

    def join(self, l_token, r_token):
        tree = Lexeme('', -1, -1, token_type = Types.JOIN)
        tree.left = l_token
        tree.right = r_token
        return tree

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
        if self.check(Types.UNKNOWN):
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

        returning = self.curr_token
        self.advance()
        return returning


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
        tree = self.match(Types.colon)
        tree.left = self.match(Types.newline)
        if self.curr_token and not self.indent(self.curr_token.col_no):
            raise ParseError("Unexpected indention level on line %d, "
                "got %s expecting %d" % (
                    self.curr_token.line_no,
                    self.curr_token.col_no,
                    self.indent_level[-1])
                )

        return tree

    def end_nest(self):
        if self.curr_token and not self.dedent(self.curr_token.col_no):
            raise ParseError("Unexpected indention level on line %d, "
                "got %s expecting %d" % (
                    self.curr_token.line_no,
                    self.curr_token.col_no,
                    self.indent_level[-1])
                )

    def program(self):
        return self.opt_form_list()

    def form_list(self):
        return self.join(self.form(), self.opt_form_list())

    def form_block(self):
        tree = self.start_nest()
        tree.right = self.form_list()
        self.end_nest()

        return tree

    def opt_form_list(self):
        tree = None
        if self.formPending() and self.newlinePending():
            tree = self.join(self.form(), self.opt_form_list())

        return tree

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
            formtree = self.defn()
        #elif self.exprPending():
        else:
            formtree = self.expr()

        #print("FORMEND"+" "+str(self.newline_seen))
        nl = None
        if not self.newline_seen:
            nl = self.match(Types.newline)

        return self.join(formtree, nl)

    def defn(self):
        tree = self.match(Types.kw_def)
        tree.left = self.variable()
        tree.right = self.form_block()

        return tree

    def variable(self):
        return self.match(Types.variable)

    def expr(self):
        if self.proc_callPending():
            return self.proc_call()
        elif self.if_exprPending():
            return self.if_expr()
        elif self.lambda_exprPending():
            return self.lambda_expr()
        elif self.set_exprPending():
            return self.set_expr()
        elif self.literalPending():
            return self.literal()
        else:
            return self.variable()

    def literal(self):
        if self.integerPending():
            return self.match(Types.integer)
        elif self.stringPending():
            return self.match(Types.string)
        elif self.tuplePending():
            return self.tuple()
        else:
            return self.quote_expr()

    def quote_expr(self):
        tree = self.match(Types.quote)
        tree.right = self.datum()

        return tree

    def datum(self):
        if self.integerPending():
            return self.match(Types.integer)
        elif self.stringPending():
            return self.match(Types.string)
        elif self.tuplePending():
            return self.tuple()
        else:
            # for symbols?
            return self.variable()

    def tuple(self):
        tree = self.match(Types.obracket)
        tree.right = self.opt_datum_list()
        tree.left = self.match(Types.cbracket)

        return tree

    def opt_datum_list(self):
        tree = None
        if self.datumPending():
            self.join(self.datum(), self.opt_datum_list())

        return tree

    def if_expr(self):
        tree = self.match(Types.kw_if)
        self.match(Types.oparen)
        tree.left = self.expr()
        self.match(Types.cparen)
        tree.right = self.join(self.form_block(),
                self.join(self.opt_elifs(), self.opt_else()))

        return tree


    def opt_elifs(self):
        tree = None
        if self.elifPending():
            tree = self.match(Types.kw_elif)
            self.match(Types.oparen)
            tree.left = self.expr()
            self.match(Types.cparen)
            tree.right = self.join(self.form_block(), self.opt_elifs())

        return tree

    def opt_else(self):
        tree = None
        if self.elsePending():
            tree = self.match(Types.kw_else)
            tree.right = self.form_block()

        return tree

    def lambda_expr(self):
        tree = self.match(Types.kw_lambda)
        if self.parametersPending():
            tree.left = self.parameters()
        tree.right = self.form_block()

        return tree

    def set_expr(self):
        tree = self.match(Types.kw_set)
        tree.left = self.variable()
        tree.right = self.form_block()

        return tree

    def proc_call(self):
        tree = self.match(Types.variable)
        tree.left = self.match(Types.oparen)
        tree.right = self.opt_expr_list()
        self.match(Types.cparen)

        return tree

    def opt_expr_list(self):
        tree = None
        if self.exprPending():
            tree = self.join(self.expr(), self.opt_expr_list())

        return tree

    def parameters(self):
        tree = self.match(Types.oparen)
        tree.left = self.join(self.variable(), self.opt_variable_list())
        tree.right = self.match(Types.cparen)

        return tree

    def opt_variable_list(self):
        tree = None
        if self.variablePending():
            tree = self.join(self.variable(), self.opt_variable_list())

        return tree

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

