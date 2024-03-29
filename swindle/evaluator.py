# evaluator.py
#
# author: Christopher S. Corley

import os
import sys
import math
from io import StringIO

from swindle.builtins import (Closure, Plosure)
from swindle.types import Types
from swindle.lexer import Lexer
from swindle.parser import Parser
from swindle.environment import SetupEnvironment

def eval_file(source, argv=sys.argv, destination=sys.stdout):
    if type(source) != str or len(source) == 0:
        return False

    try:
        with open(source) as f:
            lexer = Lexer(f)
            parser = Parser(lexer)
            tree = parser.program()
            e = Evaluator(argv)
            e.eval(tree, e.global_env.env_extend())


    except Exception as e:
        destination.write(str(e))
        destination.write('\n')
        return False

    return True


class EvalError(Exception):
     def __init__(self, value, tree):
         self.tree = tree
         self.message = value
         self.string = "ERROR on line %d, column %d:\n\t %s" % (tree.line_no, tree.col_no, value)
     def __str__(self):
         return self.string

class Evaluator:
    def __init__(self, args=None):
        self.args = args
        self.global_env = SetupEnvironment(args)
        self.repl_env = self.global_env.env_extend()

    def eval_swndl(self, text):
        l = Lexer(StringIO(text))
        p = Parser(l)
        tree = p.program()
        return self.eval(tree, self.repl_env)

    def eval(self, tree, env):
        if tree is None:
            return

        t = tree.val_type

        if t == Types.kw_def:
            return self.eval_def(tree, env)
        elif t == Types.kw_lambda:
            return self.eval_lambda(tree, env)
        elif t == Types.kw_set:
            return self.eval_set(tree, env)
        elif t == Types.kw_if:
            return self.eval_if(tree, env)
        elif t == Types.kw_elif:
            return self.eval_if(tree, env)
        elif t == Types.kw_else:
            return self.eval_else(tree, env)
        elif t == Types.colon:
            return self.eval(tree.right, env)
        elif t == Types.form_list:
            return self.eval_form_list(tree, env)
        elif t == Types.obracket:
            return self.eval_tuple(tree, env)
        elif t == Types.quote:
            return self.eval_quote(tree, env)
        elif t == Types.newline:
            pass
        elif t == Types.integer:
            return int(tree.val)
        elif t == Types.string:
            return str(tree.val)[1:-1]
        elif t == Types.symbol:
            return str(tree.val)
        elif t == Types.variable:
            # proc_call
            if tree.left and tree.left.val_type == Types.oparen:
                return self.eval_proc_call(tree, env)

            if tree.left and tree.left.val_type == Types.dot:
                return self.eval_dot_call(tree, env)

            return self.eval_variable(tree, env)
        elif t == Types.form:
            return self.eval(tree.left, env)
        else:
            raise Exception("Bad expression!")

    def eval_def(self, tree, env):
        var = tree.left.val
        val = self.eval(tree.right, env)
        env.env_insert(var, val)

    def eval_lambda(self, tree, env):
        return Closure(parameters=self.get_params(tree.left), body=tree.right, env=env)

    def get_params(self, tree):
        p = list()
        # sometimes the tree can be empty
        if tree:
            t = tree
            while t:
                p.append(t.left.val)
                t = t.right

        return p

    def eval_set(self, tree, env):
        var = tree.left.val
        val = self.eval(tree.right, env)
        env.env_update(var, val)

    def eval_if(self, tree, env):
        if self.eval(tree.left, env):
            return self.eval(tree.right.left, env)
        else:
            return self.eval(tree.right.right, env)

    def eval_else(self, tree, env):
        return self.eval(tree.right, env)

    def eval_form_list(self, tree, env):
        result = None

        t = tree
        while t:
            result = self.eval(t.left, env)
            t = t.right

        return result

    def get_expr_list(self, tree):
        # not sure about this
        # expr_list is really a list of args for proc_call
        e = list()
        # sometimes the tree can be empty
        if tree:
            t = tree.right

            while t:
                e.append(t.left)
                t = t.right

        return e

    def eval_datum_list(self, tree, env):
        # not sure about this
        d = list()

        # sometimes the tree can be empty
        if tree:
            t = tree.right

            while t:
                d.append(self.eval(t.left, env))
                t = t.right

        return d

    def eval_quote(self, tree, env):
        return self.eval(tree.right, env)

    def eval_tuple(self, tree, env):
        # maybe convert this to a list structure of cons?
        return list(self.eval_datum_list(tree, env))

    def eval_variable(self, tree, env):
        return env.env_lookup(tree.val)

    def eval_args(self, args, env):
        e = list()
        for arg in args:
            e.append(self.eval(arg, env))
        return e

    def eval_proc_call(self, tree, env):
    #    closure = self.eval(getFuncCallName(t),env);
    #    args = getFuncCallArgs(t);
    #    params = getClosureParams(closure);
    #    body = getClosureBody(closure);
    #    senv = getClosureEnvironment(closure);
    #    eargs = evalArgs(args,env);
    #    xenv = EnvExtend(senv,params,eargs);

        closure = env.env_lookup(tree.val)
        args = self.get_expr_list(tree)
        eargs = self.eval_args(args, env)
        if type(closure) == Plosure:
            # this star is very important since Guido is an idiot.
            # it's the equivalent of using apply(procedure, args) in Py2
            return closure.procedure(*eargs)
        elif type(closure) == Closure:
            params = closure.parameters
            body = closure.body
            senv = closure.env

            pairs = list()
            if len(params) > len(eargs):
                raise EvalError("Not enough arguments to call %s" % tree.val, tree)
            elif len(params) < len(eargs):
                raise EvalError("Too many arguments to call %s" % tree.val, tree)

            for i in range(0, len(params)):
                pairs.append((params[i], eargs[i]))

            xenv = senv.env_extend(pairs)
            xenv.env_insert('self', xenv)

            return self.eval(body,xenv);

    def eval_dot_call(self, tree, env):
        obj = env.env_lookup(tree.val)
        return self.eval(tree.right, obj)
