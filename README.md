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
* detection of variables used before definition ✔

### Feature examples
#### comments

Comments operate just like Python's `#` comments. There are no block comments.

    print("This is a message!") # This prints a message to console

#### integers and strings

Strings are anything between two double quotes. Integers are just
integers. You can convert between the two using `str` and `int`
(see [Builtins](#Built-ins)).

    "Hello"     => "Hello"
    5           => 5
    str(5)      => "5"
    int("5")    => 5
    
#### classes/objects

Objects are not supported.

#### arrays with O(1) access time

There are two kinds of lists: one made of cons, and arrays.

    array(5 4 3 2 1)    => [5, 4, 3, 2, 1]

There are two ways to access arrays: `get_item` and `set_item` (see [Builtins](#Built-ins))
For example, lets assume we have an array named `ar`.

    ar                  => [5, 4, 3, 2, 1]
    get_item(ar 0)      => 5
    set_item(ar 0 "5")  => ["5", 4, 3, 2, 1]

#### conditionals

Conditionals are achieved through if/elif/else.

    if (equal(a b c)):
        print("All items are the same!")
    elif (equal(a b)):
        print("a is different than c!")
    elif (equal(a c)):
        print("a is different than b!")
    else:
        print("b is different than c!")

Note that this structure behaves exactly like Python's if/elif/else.

#### recursion

Before we can talk about recursion, we need to talk about how to
define variables and functions!

##### variables

To define a variable, we use the `def` keyword.

    def five:
        5
    
    def a_string:
        "Hey, y'all!"
        
Note that this is *not* how Python's variable definition works. In fact,
it should look a whole lot like Python's function defintion, but it is *not*
that either.

##### functions

Functions are declared by using `lambda`.

    lambda (x):
        x
        
The lambda above returns a closure that accepts one parameter, `x`, and 
simply returns x. Note that returning is implicit. To use this closure,
we could assign it to some variable.

    def print_and_return:
        lambda (x):
            print(x)
            x


##### Recursion

Recursion is achieved by calling a function within itself. Here
is an example of how a recursive factorial could be implemented.

    def fact:
        lambda (n):
            if ( gt(n 1)):
                mul(n fact(sub(n 1)))
            else:
                n

    print(fact(3) fact(4) fact(5))

This would indeed print `6 20 120` to console.

#### iteration

Iteration also is achieved through recursion calls. 
*Swindle does not properly support tail call optimization at the moment*.
An iterative factorial could be implemented as so:

    def ifact:
        lambda(n):
            def iter:
                lambda (n cur):
                    if (equal(n 0)):
                        cur
                    else:
                        iter(sub(n 1) mul(n cur))   # the iterative call
            iter(n 1)

    print(ifact(3) ifact(4) ifact(5))
    
Note that functions themselves can have functions declared inside of them,
and used locally.

#### convenient means to print to the console 

If you haven't figured it out yet, you simply make a call with `print`!
It's just a call to Python's `print`, so it'll print whatever you give it.

#### an adequate set of operators

See the [Builtins](#Built-ins) section.

#### functions as first-class objects 

Functions can be tossed around just as if they were data.
For example, `cons`, `car` and `cdr` could be implemented as so:

    def my_cons:
        lambda (x y):
            lambda (i):
                if (equal(i 1)):
                    x
                elif (equal(i 2)):
                    y
    
    def my_car:
        lambda (cell):
            cell(1)
            
    def my_cdr:
        lambda (cell):
            cell(2)
            
What's going on? Here, `my_cons` is actually returning another closure with one parameter, `i`, 
that in turn picks which of the two cells, `x` or `y` to return. This closure is the cons 
cell. When `my_car` or `my_cdr` recieves a cons cell, it asks it to pick the first or second 
item, respectively.

#### an inheritance system 

No.

#### detection of variables used before definition 

The parser will detect when you use a variable before it's ever defined.
However, if one of these variables is used in a function call, it will
not be scoped correctly. Example of what it cannot detect:

    def f:
        lambda:
            a()
            b()
                    
    def a:
        lambda:
            def b:
                lambda:
                    "Haha f() can't find me!"
                    
                    

This will pass the parser, but the evaluator will fail because `f` does not have
access to `b`, which is inside `a`. 
            

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

### LISP lists and more

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
    * Create an array (a Python list) out of the arguments.
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
