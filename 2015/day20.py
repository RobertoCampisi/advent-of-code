import sys
import os
from functools import cache, reduce
import itertools
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day20.txt','r') as input_file:
        return int(input_file.read().strip())

primes = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
           53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 
           109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 
           173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 
           233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 
           293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
           367, 373, 379, 383, 389, 397, 401, 409, 419,	421, 431, 
           433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 
           499, 503, 509, 521, 523, 541]

@cache
def solve(goal, p_index = len(primes) - 1):
    if p_index < 0:
        return goal
    p = primes[p_index]
    p_power = 1
    p_sum = 1
    best = solve(goal, p_index - 1)
    while p_sum < goal:
        p_power = p_power * p
        p_sum = p_sum + p_power
        subgoal = (goal + p_sum - 1) // p_sum
        best = min(best, p_power * solve(subgoal, p_index - 1))
    return best

def factorGen(n):
    for p in primes:
        i = 1
        while n % (p ** i) == 0:
            i += 1
        if i > 1:
            yield (p,i-1)

def divisorGen(n):
    factors = list(factorGen(n))
    nf = len(factors)
    f = [0] * nf
    if nf > 0:
        while True:
            yield reduce(lambda x, y: x*y, [factors[x][0]**f[x] for x in range(nf)], 1)
            i = 0
            while True:
                f[i] += 1
                if f[i] <= factors[i][1]:
                    break
                f[i] = 0
                i += 1
                if i >= nf:
                    return
    else:
        yield 1
        yield n

def part_one():
    print(solve(parse_input()//10))


def part_two():
    goal = parse_input()
    n = solve(goal//10) #lower-bound
    max_houses = 50
    while True:
        presents = 0
        for i in divisorGen(n):
            if i * max_houses >= n:
                presents += i * 11
            else: 
                continue
        if presents >= goal:
            print(n)
            break
        else:
            n += 1

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