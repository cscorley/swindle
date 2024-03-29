import sys
from collections import namedtuple

Closure = namedtuple('closure', 'parameters body env')
Plosure = namedtuple('plosure', 'procedure')
Cons = namedtuple('cons', 'left right')

def reader(*args):
    if len(args) == 0:
        stuff = input()
    else:
        if len(args[0]) == 0:
                stuff = sys.stdin.read().rstrip()
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

def and_op(*args):
    tmp = True
    for arg in args:
        if tmp:
            tmp = (tmp and arg)
        else:
            return False
    return tmp

def or_op(*args):
    tmp = False
    for arg in args:
        if tmp:
            return True
        else:
            tmp = (tmp or arg)

    return tmp

def not_op(x):
    return not x

def sub(*args):
    tmp = None
    for arg in args:
        if tmp is not None:
            tmp = tmp - arg
        else:
            tmp = arg
    return tmp

def add(*args):
    tmp = None
    for arg in args:
        if tmp is not None:
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
        if tmp is not None:
            tmp = tmp / arg
        else:
            tmp = arg
    return tmp

def equal(*args):
    tmp = None
    result = True
    for arg in args:
        if tmp is not None:
            if not (tmp == arg):
                return False
        else:
            tmp = arg

    return True

def make_list(args, separator=None):
    if type(args) is str:
        if separator:
            args = args.split(separator)
        else:
            args = list(args)

    args.reverse()
    tmp = None
    for arg in args:
        tmp = cons(arg, tmp)

    return tmp

def make_array(*args):
    tmp = list()
    for arg in args:
        tmp.append(arg)

    return tmp


def get_item(l, position):
    # cons are not O(1)
    if type(l) is Cons:
        item = l
        while position > 0:
            item = cdr(item)
        return item

    # normal list stuff is
    return l[position]

def set_item(l, position, item):
    if type(l) is Cons:
        raise ValueError("Cannot set_item on a cons")

    l[position] = item
    return l

def set_car(c, item):
    if type(c) is Cons:
        return Cons(item, cdr(c))
    else:
        c[0] = item
        return c

def set_cdr(c, item):
    if type(c) is Cons:
        return Cons(car(c), item)
    else:
        c[1] = item
        return c


def cons(left, right):
    return Cons(left, right)

def car(c):
    if type(c) is Cons:
        return c.left

    return c[0]

def cdr(c):
    if type(c) is Cons:
        return c.right

    return c[1:]

def mixin(objects):
    child = car(objects)
    set_enclosing_scope(objects[-1], child.parent)
    chain_scopes(child, cdr(objects))
    set_definition_scopes(cdr(objects), child)
    return child

def set_enclosing_scope(item, child):
    item.parent = child

def get_enclosing_scope(item):
    return item.parent

def chain_scopes(first, rest):
    while rest:
        set_enclosing_scope(first, car(rest))
        chain_scopes(car(rest), cdr(rest))
        rest = cdr(rest)

def set_definition_scopes(scopes, child):
    for scope in scopes:
        for var, val in scope.items():
            if type(val) is Closure:
                scope[var] = Closure(val.parameters, val.body, child)

def new(child):
    return mixin(follow_parents(child))

def follow_parents(child):
    current = child
    parents = [child]
    while "parent" in current:
        parents.append(current["parent"])
        current = current["parent"]

    return parents
