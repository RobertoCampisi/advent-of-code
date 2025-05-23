import operator
from math import log
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2024/input/day07.txt','r') as input_file:
        lines = input_file.read().strip().split("\n")
        return [(int(line.split(':')[0]), list(map(int, line.split(':')[1].split()))) for line in lines]

#concat two integers without type casting
def fast_int_concat(a,b):
    return 10**int(log(b, 10)+1)*a+b

#recursive function to evaluate the whole list
def evaluable_eq(res, arr, ops):
    #base case
    if len(arr) == 1:
        return res == arr[0]
    return any((evaluable_eq(res, [op(arr[0], arr[1])] + arr[2:], ops) for op in ops))

def part_one():
    operators = [operator.mul, operator.add]
    equations = parse_input()
    total = 0
    for eq in equations:
        if evaluable_eq(eq[0], eq[1], operators):
            total += eq[0]
    print(total)

def part_two():
    operators = [operator.mul, operator.add, fast_int_concat]
    equations = parse_input()
    total = 0
    for eq in equations:
        if evaluable_eq(eq[0], eq[1], operators):
            total += eq[0]
    print(total)

#simple benchmark function.
def benchmark(func, n):
    from time import time_ns
    start = time_ns() // 1_000 #microseconds
    sys.stdout = None  # bit hacky but it works
    for i in range(0, int(n)):
        globals()[func]()
    sys.stdout = sys.__stdout__ #restore stdout
    end = time_ns() // 1_000 #microseconds
    print((end - start) / int(n) / 1000, end='')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        globals()[sys.argv[1]]()
    elif len(sys.argv) > 2:
        globals()[sys.argv[1]](*sys.argv[2:])
    else:
        raise RuntimeError