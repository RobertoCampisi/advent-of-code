import sys
import os
import re
from collections import defaultdict
from itertools import permutations

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day13.txt','r') as input_file:
        vertices = set()
        edges = defaultdict(lambda: 0)
        for line in input_file.read().split('\n'):
            words = line[:-1].split(' ')
            vertices.add(words[0])
            vertices.add(words[-1])
            unsigned_happiness = int(re.search(r'\d+',line)[0])
            if 'gain' in words[1:-1]:
                edges[(words[0], words[-1])] = edges[(words[0], words[-1])] + unsigned_happiness
                edges[(words[-1], words[0])] = edges[(words[-1], words[0])] + unsigned_happiness
            elif 'lose' in words[1:-1]:
                edges[(words[0], words[-1])] = edges[(words[0], words[-1])] - unsigned_happiness
                edges[(words[-1], words[0])] = edges[(words[-1], words[0])] - unsigned_happiness
        return vertices, edges

def part_one():
    guests, happiness = parse_input()
    max_happiness = 0
    for seating_arrangement in permutations(guests,len(guests)):
        total_happiness = 0
        for g1, g2 in zip(seating_arrangement[:-1], seating_arrangement[1:]):
            total_happiness += happiness[(g1,g2)]
        total_happiness += happiness[(seating_arrangement[-1], seating_arrangement[0])]
        if total_happiness > max_happiness:
            max_happiness = total_happiness
    print(max_happiness)


def part_two():
    guests, happiness = parse_input()
    for g in guests:
        happiness[('I',g)] = 0
        happiness[(g,'I')] = 0
    guests.add('I')
    max_happiness = 0
    for seating_arrangement in permutations(guests, len(guests)):
        total_happiness = 0
        for g1, g2 in zip(seating_arrangement[:-1], seating_arrangement[1:]):
            total_happiness += happiness[(g1, g2)]
        total_happiness += happiness[(seating_arrangement[-1], seating_arrangement[0])]
        if total_happiness > max_happiness:
            max_happiness = total_happiness
    print(max_happiness)

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