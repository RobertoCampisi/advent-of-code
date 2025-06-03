import re
import sys
import os
from math import prod
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day15.txt','r') as input_file:
        properties = []
        for line in input_file.read().split('\n'):
            properties.append(list(map(int,re.findall(r'-*\d+',line))))
        return properties

def teaspoon_gen_rec(res, total_sum, depth):
    if depth == 1:
        yield res + [total_sum]
    else:
        for a in range(total_sum + 1):
            yield from teaspoon_gen_rec(res + [a], total_sum - a, depth - 1)

def part_one():
    properties = parse_input()
    best_total_score = 0
    for n in teaspoon_gen_rec([],100,len(properties)):
        property_scores = [0]*len(properties[0])
        for i,t in enumerate(n):
            for j, p in enumerate(properties[i]):
                property_scores[j] += t * p
        property_scores = [max(0,p) for p in property_scores]
        new_total_score = prod(property_scores[:-1]) #ingore last property calories
        if new_total_score > best_total_score:
            best_total_score = new_total_score
    print(best_total_score)

def part_two():
    properties = parse_input()
    best_total_score = 0
    for n in teaspoon_gen_rec([], 100, len(properties)):
        property_scores = [0] * len(properties[0])
        for i, t in enumerate(n):
            for j, p in enumerate(properties[i]):
                property_scores[j] += t * p
        if property_scores[-1] != 500:
            continue
        property_scores = [max(0, p) for p in property_scores]
        new_total_score = prod(property_scores[:-1])  # ingore last property calories
        if new_total_score > best_total_score:
            best_total_score = new_total_score
    print(best_total_score)

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