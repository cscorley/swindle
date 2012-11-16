# scanner.py
#
# author: Christopher S. Corley

import os
import sys
from swindle.types import Types
from swindle.lexeme import Lexeme
from swindle.environment import (Environment, EnvironmentLookupError, DebugEnvironment)

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

        # variable forwarding detection stack
        self.delays = list()


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

    def newlinePending(self):
        val = self.newline(self.curr_token.col_no)
        #print("NLP "+str(val)+" "+str(self.newline_seen))
        return val

    def formPending(self):
        val = (self.exprPending() or self.defnPending())
        #print("FORM %s %s" % (str(val), str(self.curr_token)))
        return val

    def program(self):
        e = DebugEnvironment()
        return self.opt_form_list(e)

    def form_list(self, env):
        return self.join(self.form(env), self.opt_form_list(env))

    def form_block(self, env):
        tree = self.start_nest()
        tree.right = self.form_list(env)
        self.end_nest()

        return tree

    def opt_form_list(self, env):
        tree = None
        if self.formPending() and self.newlinePending():
            tree = self.join(self.form(env), self.opt_form_list(env))

        return tree


    def form(self, env):
        if self.defnPending():
            formtree = self.defn(env)
        #elif self.exprPending():
        else:
            formtree = self.expr(env)

        #print("FORMEND"+" "+str(self.newline_seen))
        nl = None
        if not self.newline_seen:
            nl = self.match(Types.newline)

        return self.join(formtree, nl)

    def defn(self, env):
        tree = self.match(Types.kw_def)
        tree.left = self.variable_decl(env)
        tree.right = self.form_block(env)

        return tree

    def variable_use(self, env):
        var = self.match(Types.variable)
        env.env_lookup(var.val)
        return var

    def variable_call(self, env):
        var = self.match(Types.variable)
        try:
            env.env_lookup(var.val)
        except EnvironmentLookupError as e:
            self.delays.append(var)
            #raise ParseError(str(e))
        return var

    def variable_decl(self, env):
        var = self.match(Types.variable)
        env.env_insert(var.val, var.val)
        return var

    def variable_set(self, env):
        var = self.match(Types.variable)
        env.env_update(var.val, var.val)
        return var

    def expr(self, env):
        if self.proc_callPending():
            return self.proc_call(env)
        elif self.if_exprPending():
            return self.if_expr(env)
        elif self.lambda_exprPending():
            return self.lambda_expr(env)
        elif self.set_exprPending():
            return self.set_expr(env)
        elif self.literalPending():
            return self.literal(env)
        else:
            return self.variable_use(env)

    def literal(self, env):
        if self.integerPending():
            return self.match(Types.integer)
        elif self.stringPending():
            return self.match(Types.string)
        elif self.tuplePending():
            return self.tuple(env)
        else:
            return self.quote_expr(env)

    def quote_expr(self, env):
        tree = self.match(Types.quote)
        tree.right = self.datum(env)

        return tree

    def datum(self, env):
        if self.integerPending():
            return self.match(Types.integer)
        elif self.stringPending():
            return self.match(Types.string)
        elif self.tuplePending():
            return self.tuple(env)
        else:
            # for symbols?
            return self.variable_use(env)

    def tuple(self, env):
        tree = self.match(Types.obracket)
        tree.right = self.opt_datum_list(env)
        tree.left = self.match(Types.cbracket)

        return tree

    def opt_datum_list(self, env):
        tree = None
        if self.datumPending():
            self.join(self.datum(env), self.opt_datum_list(env))

        return tree

    def if_expr(self, env):
        tree = self.match(Types.kw_if)
        self.match(Types.oparen)
        tree.left = self.expr(env)
        self.match(Types.cparen)
        tree.right = self.join(self.form_block(env),
                self.join(self.opt_elifs(env), self.opt_else(env)))

        return tree


    def opt_elifs(self, env):
        tree = None
        if self.elifPending():
            tree = self.match(Types.kw_elif)
            self.match(Types.oparen)
            tree.left = self.expr(env)
            self.match(Types.cparen)
            tree.right = self.join(self.form_block(env), self.opt_elifs(env))

        return tree

    def opt_else(self, env):
        tree = None
        if self.elsePending():
            tree = self.match(Types.kw_else)
            tree.right = self.form_block(env)

        return tree

    def lambda_expr(self, env):
        tree = self.match(Types.kw_lambda)
        local_env = env.env_extend()
        if self.parametersPending():
            tree.left = self.parameters(local_env)
        tree.right = self.form_block(local_env)

        return tree

    def set_expr(self, env):
        tree = self.match(Types.kw_set)
        tree.left = self.variable_set(env)
        tree.right = self.form_block(env)

        return tree

    def proc_call(self, env):
        tree = self.variable_call(env)
        tree.left = self.match(Types.oparen)
        tree.right = self.opt_expr_list(env)
        self.match(Types.cparen)

        return tree

    def opt_expr_list(self, env):
        tree = None
        if self.exprPending():
            tree = self.join(self.expr(env), self.opt_expr_list(env))

        return tree

    def parameters(self, env):
        tree = self.match(Types.oparen)
        tree.left = self.join(self.variable_decl(env), self.opt_variable_list(env))
        tree.right = self.match(Types.cparen)

        return tree

    def opt_variable_list(self, env):
        tree = None
        if self.variablePending():
            tree = self.join(self.variable_decl(env), self.opt_variable_list(env))

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

