import sys
import os
from collections import defaultdict
import re
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day06.txt','r') as input_file:
        instructions = []
        for line in input_file.read().split('\n'):
            numbers = re.findall(r'(\d+)', line)
            if numbers:
                s1, s2, e1, e2 = list(map(int,numbers))
                if re.search(r'turn on', line):
                    instructions.append((1,(s1,s2),(e1,e2)))
                if re.search(r'turn off', line):
                    instructions.append((2,(s1,s2),(e1,e2)))
                if re.search(r'toggle', line):
                    instructions.append((3,(s1,s2),(e1,e2)))
        return instructions


def part_one():
    lights = defaultdict(bool)
    for line in parse_input():
        ins, start, end = line
        light_range = [x+y*1j for y in range(start[1], end[1] + 1) for x in range(start[0], end[0] + 1)]
        match ins:
            case 1: 
                for i in light_range: 
                    lights[i] = True
            case 2: 
                for i in light_range: 
                    lights[i] = False
            case 3:
                for i in light_range: 
                    lights[i] = not lights[i]
            case _: ...
    print(sum(lights.values()))

def part_two():
    lights = defaultdict(int)
    for line in parse_input():
        ins, start, end = line
        light_range = [x+y*1j for y in range(start[1], end[1] + 1) for x in range(start[0], end[0] + 1)]
        match ins:
            case 1: 
                for i in light_range: 
                    lights[i] += 1
            case 2: 
                for i in light_range: 
                    lights[i] = max(0,lights[i]-1)
            case 3:
                for i in light_range: 
                    lights[i] += 2
            case _: ...
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