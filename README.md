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

Language
========

### A LISP-like with Python syntax? What is wrong with you?

A lot. Much of the LISP syntax has been replaced with Python
equivalents. There is a lot of functionality missing. This was
implemented for a course on programming languages.

### Required features (and TODO list)

* comments ✔
* integers and strings ✔
* classes/objects ✗
* arrays with O(1) access time ✔
* conditionals ✔
* recursion ✔
* iteration ✓ (no tail call optimization)
* convenient means to print to the console ✔
* an adequate set of operators ✔
* functions as first-class objects ✔
* an inheritance system ✗
* detection of variables used before definition ✓ (partial)

Example program
---------------

    def abs:
        lambda (x):
            if ( lt(x 0) ):
                neg(x)
            else:
                x

    abs(neg(4))

More example programs can be found in `tests/case/` (note that improper
programs are prepended with 'bad_')

Built-ins
---------

### System
* `len(item)`
    * Returns an integer of the length of the given array
    * Does not work with `cons` lists.
    * Same as Python's
      [len](http://docs.python.org/3/library/functions.html#len)
* `str(item)`
    * Returns a string representation of the given item
    * Same as Python's
      [str](http://docs.python.org/3/library/functions.html#str)
* `int(item)`
    * Returns an integer representation of the given item
    * Same as Python's
      [int](http://docs.python.org/3/library/functions.html#int)
* `print(item)`
    * Can be used to print to console
    * Same as Python's
      [print](http://docs.python.org/3/library/functions.html#print)
* `input(*args)`
    * When it receives no arguments, it calls Python's
      [input](http://docs.python.org/3/library/functions.html#input)
    * When it receives arguments, if first argument is an empty Python
      list, then it reads from `sys.stdin`. Otherwise, it opens the
      first argument's first item as a file, and returns a string of
      that file's contents (if it exists).
         * (yes I realize this is crap).
* `args()`
    * Returns a Python list of arguments given to the interpreter
* `equal(*items)`
    * Compares items for equality.

### LISP

* `cons(a b)`
    * Returns a namedtuple Cons with a left and right.
* `car(c)`
    * When given a `cons`, returns `cons.left`. When given a Python
      list, returns the first element of the list.
* `cdr(c)`
    * When given a `cons`, returns `cons.right`. When given a Python
      list, returns the list slice `l[1:]` (all items except for the
      first).
* `list(items [separator])`
    * Returns a `cons` list structure of the arguments. When given a
      string, it returns a `cons` of each character. When given two
      strings, the second item is used as a separator and a `cons` is
      returned of strings.
        * String examples: `list("swndl")` gives `("s" ("w" ("n" ("d"
          ("l" None)))))`. While `list("Hello, world!" " ")` would
          tokenize the string "Hello, world!" and return `("Hello,"
          ("world!", None)`
* `set_car(c item)`
    * Sets the car of c to item
    * If given an array, will set the first item of that array to item.
* `set_cdr(c item)`
    * Sets the cdr of c to item
    * If given an array, will set the second item of that array to item
      (does not modify the rest of the array).
* `array(*args)`
    * Create an array (a Python list) out off the arguments.
* `get_item(l position)`
    * Return the item at position in l.
    * Provides O(1) access on arrays, and O(n) on cons lists.
* `set_item(l position item)`
    * Replace the item at position in l.
    * Provides O(1) access on arrays, does not operate on cons lists.

### Math
* `neg(x)`
    * Negates the number
* `lt(a b)`
    * Compares two items for `a < b`
* `gt(a b)`
    * Compares two items for `a > b`
* `add(*args)`
    * Adds all the arguments to the first item
* `sub(*args)`
    * Subtracts all the arguments from the first item
* `mul(*args)`
    * Multiplies all the arguments
* `div(*args)`
    * Divides all the arguments into the first item
* `cos(x)`
    * Returns cosine of x (in radians)
    * Same as Python's
      [math.cos](http://docs.python.org/3/library/math.html#math.cos)
* `sin(x)`
    * Returns sine of x (in radians)
    * Same as Python's
      [math.sin](http://docs.python.org/3/library/math.html#math.sin)
* `log(x [base])`
    * Returns natural log of x. A second parameter determines the base.
    * Same as Python's
      [math.log](http://docs.python.org/3/library/math.html#math.log)
* `tan(x)`
    * Returns tangent of x (in radians)
    * Same as Python's
      [math.tan](http://docs.python.org/3/library/math.html#math.tan)
* `pow(a b)`
    * Returns a raised to power b.
    * Same as Python's
      [math.pow](http://docs.python.org/3/library/math.html#math.pow)
* `factorial(x)`
    * Returns x!.
    * Same as Python's
      [math.factorial](http://docs.python.org/3/library/math.html#math.factorial)
* `sqrt(x)`
    * Returns the square root of x.
    * Same as Python's
      [math.sqrt](http://docs.python.org/3/library/math.html#math.sqrt)
