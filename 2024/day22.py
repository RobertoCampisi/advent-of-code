import sys
import os
from functools import cache
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2024/input/day22.txt','r') as input_file:
        return [int(n.strip()) for n in input_file.readlines()]
 
def sim(init, d):
    n = init
    while d > 0:
        n = next(n)
        d -= 1
    return n

def sim_part2(init, d):
    global sequences
    n = init
    delta_list, seen = [(n % 10, None)], set()
    while d > 0:
        n = next(n)
        d -= 1
        delta_list.append((n % 10, (n % 10) - delta_list[-1][0]))
        if len(delta_list) > 4:
            seq = tuple([delta_list[-j][1] for j in range(1,5)])
            if seq not in seen:
                seen.add(seq)
                sequences[seq] = sequences[seq] + [n % 10] if seq in sequences else [n % 10]
    return n

@cache
def next(n):
    n = (n ^ n << 6) % (1 << 24)
    n = (n ^ n >> 5) % (1 << 24)
    n = (n ^ n << 11)% (1 << 24)
    return n

def part_one():
    numbers = parse_input()
    print(sum(sim(n, 2000) for n in numbers))
    next.cache_clear()

def part_two():
    global sequences
    sequences = {}
    numbers = parse_input()
    for n in numbers:
        sim_part2(n,2000)
    print(max([sum(sequence) for sequence in sequences.values()]))
    next.cache_clear()

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