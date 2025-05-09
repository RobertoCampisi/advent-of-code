import sys
import os
from functools import cache
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2024/input/day19.txt','r') as input_file:
        towels, designs = input_file.read().split('\n\n')
        towels = tuple(towels.split(", "))
        designs = designs.split("\n")
        return towels, designs

def rec(d, towels, memory):
    if d in memory:
        return memory[d]
    #terminate
    if d == '':
        return 1
    total = 0
    for t in towels:
        if d.startswith(t):
            total += rec(d[len(t):], towels, memory)
    memory[d] = total
    return total
    
def part_one():
    towels, designs = parse_input()
    towel_mem = dict()
    res = 0
    for i,d in enumerate(designs):
        if rec(d,towels,towel_mem) > 0:
            res += 1
    print(res)

def part_two():
    towels, designs = parse_input()
    towel_mem = dict()
    res = 0
    for i,d in enumerate(designs):
        n = rec(d,towels,towel_mem)
        res += n
    print(res)

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