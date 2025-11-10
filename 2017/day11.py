import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2017/input/day11.txt','r') as input_file:
        return input_file.read().split(',')

def part_one():
    path = parse_input()
    origin = 0+0j
    current = origin
    dir = {'n':1j, 's':-1j, 'nw': -1+1j , 'sw': -1, 'ne': 1, 'se': 1-1j}
    for p in path:
        current += dir[p]
    print(int(abs(current.real) + abs(current.imag)))

def part_two():
    path = parse_input()
    origin = 0+0j
    current = origin
    max_distance = 0
    dir = {'n':1j, 's':-1j, 'nw': -1+1j , 'sw': -1, 'ne': 1, 'se': 1-1j}
    for p in path:
        current += dir[p]
        distance = int(abs(current.real) + abs(current.imag))
        if distance > max_distance:
            max_distance = distance
    print(max_distance)

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