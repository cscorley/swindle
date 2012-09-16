swindle
=======

A simplified LISP-like interpreter built on Python that throws away
parentheses in favor of Python-style colon and indentation on special
forms. I might be burned at the stake for this.

Grammar
=======
The grammar is written in a BNF variant.

To complete this task, I have introduced several new (magical) terms
to denote lexer tasks.
 - *newline* denotes the newline character is present
 - *indent* ensures there is more indentation up to the first
   non-whitespace character than the previous line
 - *dedent* ensures there is less or equal indentation up to the first
   non-whitespace character that when the last *indent* was performed.

*derived_expr* denotes expressions, such as cond, and, or, let, and so
on, that can be defined in terms of the primative expressions.

An example program:

    def abs:
        lambda x:
            if ( lt(x 0) ):
                -x
            else:
                x

    abs(-4)

