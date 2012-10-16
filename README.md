swindle
=======

A simplified LISP-like interpreter built on Python that throws away
parentheses in favor of Python-style colon and indentation on special
forms. I might be burned at the stake for this.

Requirements
============
`swindle` runs on Python 3.2 or above. Additional package requirements
(for unit testing) are as follows:

    distribute==0.6.28
    nose==1.2.1
    wsgiref==0.1.2

You can install these requirements by running `make init`, which
requires pip.

Running
=======
At the moment, you can run swindle by executing `bin/scanner`, or `make
run`. `make run` will also execute `bin/scanner` on all files in
`tests/case/`, but does not include the unit testing. Unit tests can be
ran by executing `make test`.

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

More example programs can be found in `tests/case/`

