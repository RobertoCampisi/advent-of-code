import itertools
import sys
import os
from collections import defaultdict
from itertools import combinations

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day17.txt','r') as input_file:
        return [int(line) for line in input_file.read().split('\n')]

def determine_bound(list_, sum_):
    total_sum = 0
    for i, b in enumerate(list_):
        total_sum += b
        if total_sum >= sum_:
            return i

def part_one():
    buckets = parse_input()
    lower_bound = determine_bound(reversed(sorted(buckets)),150)
    upper_bound = determine_bound(sorted(buckets),150)
    total_combinations = 0
    for n in range(lower_bound, upper_bound + 1):
        for c in combinations(buckets,n):
            if sum(c) == 150:
                total_combinations += 1
    print(total_combinations)


def part_two():
    buckets = parse_input()
    lower_bound = determine_bound(reversed(sorted(buckets)), 150)
    upper_bound = determine_bound(sorted(buckets), 150)
    total_combinations = defaultdict(lambda: 0)
    for n in range(lower_bound, upper_bound + 1):
        for c in combinations(buckets, n):
            if sum(c) == 150:
                total_combinations[n] += 1
    # print the minimum
    for k, v in total_combinations.items():
        if v > 0:
            print(v)
            break

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