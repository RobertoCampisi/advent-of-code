import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions
from my_utils import tadd, tsub

def parse_input():
    with open('2024/input/day8.txt','r') as input_file:
        return  input_file.read().strip().split("\n")

def in_bounds(a, w, h):
    return not (a[0] < 0 or a[0] >= w or a[1] < 0 or a[1] >= h)

def part_one():
    lines = parse_input()
    frequencies = dict()
    antinodes = set()
    w, h = len(lines[0]), len(lines)
    for y, line in enumerate(lines):
        antanas = re.finditer(r'[a-zA-Z0-9]', line)
        for a in antanas:
            pos = (a.span()[0], y)
            for o in frequencies.get(a[0], []):
                dif = tsub(pos, o)
                antinodes.add(tadd(pos, dif))
                antinodes.add(tsub(o, dif))
            # add the antanas to the frequency dictionary
            frequencies[a[0]] = frequencies.get(a[0], []) + [pos]
        # filter all antinode within bounds
        antinodes_out_bounds = set()
        for an in antinodes:
            if not in_bounds(an,w,h):
                antinodes_out_bounds.add(an)
        for anob in antinodes_out_bounds:
            antinodes.discard(anob)
    print(len(antinodes))

def part_two():
    lines = parse_input()
    frequencies = dict()
    antinodes = set()
    w, h = len(lines[0]), len(lines)
    for y, line in enumerate(lines):
        antanas = re.finditer(r'[a-zA-Z0-9]', line)
        for a in antanas:
            pos = (a.span()[0], y)
            for o in frequencies.get(a[0], []):
                dif = tsub(pos, o)
                n1 = pos
                while in_bounds(n1, w, h):
                    antinodes.add(n1)
                    n1 = tadd(n1, dif)
                n2 = tsub(pos, dif)
                while in_bounds(n2, w, h):
                    antinodes.add(n2)
                    n2 = tsub(n2, dif)
            # add the antanas to the frequency dictionary
            frequencies[a[0]] = frequencies.get(a[0], []) + [pos]
    print(len(antinodes))

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