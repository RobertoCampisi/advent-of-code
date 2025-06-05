import sys
import os
from itertools import combinations
import math
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day24.txt','r') as input_file:
        return [int(x) for x in input_file.read().split('\n')]

def find_bound(sorted_list, total_sum):
    res = 0
    for i,x in enumerate(sorted_list):
        res += x
        if res >= total_sum:
            return i
    return len(sorted_list)

def part_one():
    packets = parse_input()
    group_weight = sum(packets)//3
    lower_bound = find_bound(sorted(packets,reverse=True), group_weight)
    upper_bound = find_bound(sorted(packets), group_weight)
    lowest_qe = math.inf
    for a in range(lower_bound, upper_bound + 1):
        for group1 in combinations(packets,a):
            if sum(group1) == group_weight:
                #remainder = list(filter(lambda x: not x in group1, packets))
                #for b in range(lower_bound, upper_bound + 1 - a):
                #    for group2 in combinations(remainder, b):
                #        if sum(group2) == group_weight:
                #            qe = math.prod(group1)
                #            lowest_qe = min(lowest_qe, qe)
                # due to all numbers (except 1) being prime it no not needed to verify the other group weights
                qe = math.prod(group1)
                lowest_qe = min(lowest_qe, qe)
        if lowest_qe < math.inf:
            break
    print(lowest_qe)


def part_two():
    packets = parse_input()
    group_weight = sum(packets)//4
    lower_bound = find_bound(sorted(packets,reverse=True), group_weight)
    upper_bound = find_bound(sorted(packets), group_weight)
    lowest_qe = math.inf
    for a in range(lower_bound, upper_bound + 1):
        for group1 in combinations(packets,a):
            if sum(group1) == group_weight:
                qe = math.prod(group1)
                lowest_qe = min(lowest_qe, qe)
        if lowest_qe < math.inf:
            break
    print(lowest_qe)

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