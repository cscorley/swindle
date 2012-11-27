import sys
from collections import namedtuple

Closure = namedtuple('closure', 'parameters body env')
Plosure = namedtuple('plosure', 'procedure')

def reader(*args):
    if len(args) == 0:
        stuff = input()
    else:
        with open(args[0][0]) as f:
            stuff = f.read().rstrip()

    return stuff

def neg(num):
    return -num

def lt(a, b):
    return a < b

def gt(a, b):
    return a > b

def sub(*args):
    tmp = None
    for arg in args:
        if tmp:
            tmp = tmp - arg
        else:
            tmp = arg
    return tmp

def add(*args):
    tmp = None
    for arg in args:
        if tmp:
            tmp = tmp + arg
        else:
            tmp = arg
    return tmp

def mul(*args):
    result = 1
    for arg in args:
        result = result * arg
    return result

def div(*args):
    tmp = None
    for arg in args:
        if tmp:
            tmp = tmp / arg
        else:
            tmp = arg
    return tmp

def equal(*args):
    tmp = None
    result = True
    for arg in args:
        if tmp:
            if not (tmp == arg):
                return False
        else:
            tmp = arg

    return True

def make_list(args):
    if type(args) is str:
        args = args.split(' ')

    args.reverse()
    tmp = None
    for arg in args:
        tmp = cons(arg, tmp)

    return tmp


# http://jjinux.blogspot.com/2008/02/scheme-implementing-cons-car-and-cdr.html
def cons(a, b):
    def cell(pick):
        if pick == 1:
            return a
        elif pick == 2:
            return b
        else:
            raise ValueError

    return cell

def car(c):
    return c(1)

def cdr(c):
    return c(2)
