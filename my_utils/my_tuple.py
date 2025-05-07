import operator

#simple element wise operations on tuples.
def tadd(a, b):
    return tuple(map(operator.add, a, b))

def tsub(a, b):
    return tuple(map(operator.sub, a, b))

def tmul(a, b):
    return tuple(map(operator.mul, a, b))