import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions
from my_utils import astar

def parse_input():
    with open('2024/input/day20.txt','r') as input_file:
        start = 0
        end = 0
        lines = input_file.read().split("\n")
        h, w = len(lines), len(lines[0])
        racetrack = dict()
        for j,line in enumerate(lines):
            for i in range(len(line)):
                if line[i] == 'S':
                    start = i+j*1j
                if line[i] == 'E':
                    end = i+j*1j
                if line[i] == '#':
                    racetrack[i+j*1j] = 1
                else:
                    racetrack[i+j*1j] = 0
        return racetrack, start, end

def part_one():
    racetrack, start, end = parse_input()
    base_len = len(astar(racetrack, start, end))
    print(base_len) 

def part_two():
    ...

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