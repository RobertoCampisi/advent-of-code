import sys
import os
from math import log10
from functools import cache
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2024/input/day11.txt','r') as input_file:
        return list(map(int,(input_file.read().strip().split("\n")[0].split())))

@cache
def new_stone(stone):
    if stone == 0:
        return [1]
    elif (int(log10(stone)) + 1) % 2 == 0:
        n = int(int(log10(stone) + 1) / 2)
        return [int(stone / (10 ** n)), int(stone % (10 ** n))]
    else:
        return [2024 * stone]

@cache
def total_stones(stones, layer):
    if len(stones) == 0:
        return 0
    elif layer == 0:
        return len(stones)
    else:
        total_first_stone = total_stones(tuple(new_stone(stones[0])), layer - 1)
        return  total_first_stone + total_stones(tuple(stones[1:]), layer)

def part_one():
    arrangement = parse_input()
    print(total_stones(tuple(arrangement), 25))

def part_two():
    arrangement = parse_input()
    print(total_stones(tuple(arrangement), 75))

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