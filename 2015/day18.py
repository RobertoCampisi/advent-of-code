import sys
import os
from collections import defaultdict
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day18.txt','r') as input_file:
        lights = defaultdict(lambda: False)
        for j,line in enumerate(input_file.read().split('\n')):
            for i,light in enumerate(line):
                if light == '#':
                    lights[i+j*1j] = True
        return lights

def turn_on_corners(grid,grid_size):
    x = grid_size-1
    grid[0] = True
    grid[x * 1j] = True
    grid[x] = True
    grid[x + x * 1j] = True
    return grid

def part_one():
    lights = parse_input()
    steps = 100
    for _ in range(steps):
        new_lights = defaultdict(lambda: False)
        for j in range(100):
            for i in range(100):
                x = i+j*1j
                neighbors = sum([lights[x + p] for p in [1j, 1+1j,1,1-1j,-1j,-1-1j,-1,-1+1j]])
                if lights[x] and (neighbors == 2 or neighbors == 3):
                    new_lights[x] = True
                elif not lights[x] and neighbors == 3:
                    new_lights[x] = True
        lights = new_lights
    print(sum(lights.values()))

def part_two():
    lights = turn_on_corners(parse_input(),100)
    steps = 100
    for _ in range(steps):
        new_lights = defaultdict(lambda: False)
        for j in range(100):
            for i in range(100):
                x = i+j*1j
                neighbors = sum([lights[x + p] for p in [1j, 1+1j,1,1-1j,-1j,-1-1j,-1,-1+1j]])
                if lights[x] and (neighbors == 2 or neighbors == 3):
                    new_lights[x] = True
                elif not lights[x] and neighbors == 3:
                    new_lights[x] = True
        lights = turn_on_corners(new_lights,100)
    print(sum(lights.values()))

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