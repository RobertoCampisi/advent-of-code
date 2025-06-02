import sys
import os
from itertools import combinations, permutations

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day09.txt','r') as input_file:
        vertices = set()
        edges = dict()
        for line in input_file.read().split('\n'):
            v1, _, v2, _, weight = line.split(' ')
            vertices.add(v1)
            vertices.add(v2)
            edges[(v1, v2)] = int(weight)
            edges[(v2, v1)] = int(weight)
        return vertices, edges

def part_one():
    vertices, edges = parse_input()
    #brute force
    print(min([sum([edges[(path[i],path[i+1])] for i in range(len(path)-1)])
               for path in permutations(vertices,len(vertices))]))

def part_two():
    vertices, edges = parse_input()
    # brute force
    print(max([sum([edges[(path[i], path[i + 1])] for i in range(len(path) - 1)])
               for path in permutations(vertices, len(vertices))]))

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