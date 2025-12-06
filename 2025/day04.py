import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions
from collections import defaultdict

def parse_input():
    with open('2025/input/day04.txt','r') as input_file:
        sparse_grid = defaultdict(lambda : False)
        for j, line in enumerate(input_file.read().split('\n')):
            for i, pos in enumerate(line):
                if pos == '@':
                    sparse_grid[i+j*1j] = True
        return sparse_grid

def part_one():
    rolls = parse_input()
    access_count = 0
    neighbours = [-1+1j, 1j , 1+1j, 1, 1-1j, -1j, -1-1j, -1]
    for pos, roll in list(rolls.items()):
        if roll and sum([rolls[pos+x] for x in neighbours]) < 4:
                access_count += 1
    print(access_count)

def part_two():
    rolls = parse_input()
    access_count = 0
    neighbours = [-1 + 1j, 1j, 1 + 1j, 1, 1 - 1j, -1j, -1 - 1j, -1]
    while True:
        access_count_old = access_count
        for pos, roll in list(rolls.items()):
            if roll and sum([rolls[pos + x] for x in neighbours]) < 4:
                rolls[pos] = False
                access_count += 1
        if access_count == access_count_old:
            break
    print(access_count)

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