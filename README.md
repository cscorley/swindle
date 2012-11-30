swindle
=======

Swindle is a simplified LISP-like interpreter built on Python that
throws away parentheses in favor of Python-style colon and indentation
on special forms. I might be burned at the stake for this.

Requirements
============

`swindle` runs on Python 3.2 or above. Support for lower Python 3.x
versions has been hacked in, so use at your own risk there.

Additional package requirements for unit testing are as follows:

    nose==1.2.1

You can install these requirements by running `make install`, which
requires `pip`.

Running
=======

At the moment, you can run swindle by executing `bin/swndl`, or `make
run`. `make run` will also execute `bin/swndl` on all files in
`tests/case/`, but does not include the unit testing. Unit tests can be
ran by executing `make test`.

All test cases which fail are prepended with 'bad_' in the file name.
All other test cases should parse.


Example program
---------------

    def abs:
        lambda x:
            if ( lt(x 0) ):
                neg(x)
            else:
                x

    abs(neg(4))

More example programs can be found in `tests/case/` (note that improper
programs are prepended with 'bad_')

Built-ins
---------

Some built-in functions for your use are available in `swindle`:

### System
* `len`
    * Same as Python's
      [len](http://docs.python.org/3/library/functions.html#len)
* `str`
    * Same as Python's
      [str](http://docs.python.org/3/library/functions.html#str)
* `int`
    * Same as Python's
      [int](http://docs.python.org/3/library/functions.html#int)
* `print`
    * Same as Python's
      [print](http://docs.python.org/3/library/functions.html#print)
* `input`
    * When it receives no arguments, it calls Python's
      [input](http://docs.python.org/3/library/functions.html#input)
    * When it receives arguments, if first argument is an empty Python
      list, then it reads from `sys.stdin`. Otherwise, it opens the
      first argument's first item as a file, and returns a string of
      that file's contents (if it exists).
         * (yes I realize this is crap).
* `args`
    * Returns a Python list of arguments given to the interpreter
* `equal`
    * Compares two items for equality.

### LISP

* `cons`
    * Returns a namedtuple Cons with a left and right.
* `car`
    * When given a `cons`, returns `cons.left`. When given a Python
      list, returns the first element of the list.
* `cdr`
    * When given a `cons`, returns `cons.right`. When given a Python
      list, returns the list slice `l[1:]` (all items except for the
      first).
* `list`
    * Returns a `cons` list structure of the arguments. When given a
      string, it returns a `cons` of each character. When given two
      strings, the second item is used as a separator and a `cons` is
      returned of strings.
        * String examples: `list("swndl")` gives `("s" ("w" ("n" ("d"
          ("l" None)))))`. While `list("Hello, world!" " ")` would
          tokenize the string "Hello, world!" and return `("Hello,"
          ("world!", None)`

### Math
* `neg`
    * Negates the number
* `lt`
    * Compares two items for `a < b`
* `gt`
    * Compares two items for `a > b`
* `add`
    * Adds all the arguments to the first item
* `sub`
    * Subtracts all the arguments from the first item
* `mul`
    * Multiplies all the arguments
* `div`
    * Divides all the arguments into the first item
* `cos`
    * Same as Python's
      [math.cos](http://docs.python.org/3/library/math.html#math.cos)
* `sin`
    * Same as Python's
      [math.sin](http://docs.python.org/3/library/math.html#math.sin)
* `log`
    * Same as Python's
      [math.log](http://docs.python.org/3/library/math.html#math.log)
* `tan`
    * Same as Python's
      [math.tan](http://docs.python.org/3/library/math.html#math.tan)
* `pow`
    * Same as Python's
      [math.pow](http://docs.python.org/3/library/math.html#math.pow)
* `factorial`
    * Same as Python's
      [math.factorial](http://docs.python.org/3/library/math.html#math.factorial)
* `sqrt`
    * Same as Python's
      [math.sqrt](http://docs.python.org/3/library/math.html#math.sqrt)
