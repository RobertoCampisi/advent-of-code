import sys
import os
from collections import defaultdict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2025/input/day07.txt','r') as input_file:
        lines = input_file.read().split('\n')
        grid = defaultdict(lambda : False)
        width = len(lines[0])
        height = len(lines)
        start = 0
        for j, line in enumerate(lines):
            for i, character in enumerate(line):
                if character == '^':
                    grid[i+j*1j] = True
                if character == 'S':
                    start = i
        return grid, width, height, start

def part_one():
    manifold , width, height, start = parse_input()
    beams = [False] * width
    beams[start] = True
    split_counter = 0
    for j in range(height):
        new_beams = [False] * width
        for i in range(width):
            if beams[i]:
                if manifold[i+(j+1)*1j]:
                    split_counter += 1
                    new_beams[i] = False
                    new_beams[i-1] = True
                    new_beams[i+1] = True
                else:
                    new_beams[i] = True
        #print(''.join(['|' if beams[i] else '^' if manifold[i + j * 1j] else '.' for i in range(width)]))
        beams = new_beams
    print(split_counter)

def part_two():
    manifold, width, height, start = parse_input()
    beams = [False] * width
    beams[start] = 1
    split_counter = 0
    for j in range(height):
        new_beams = [0] * width
        for i in range(width):
            if beams[i] > 0:
                if manifold[i + (j + 1) * 1j]:
                    split_counter += 1
                    new_beams[i] = 0
                    new_beams[i - 1] += beams[i]
                    new_beams[i + 1] += beams[i]
                else:
                    new_beams[i] += beams[i]
        # print(''.join(['|' if beams[i] else '^' if manifold[i + j * 1j] else '.' for i in range(width)]))
        beams = new_beams
    print(sum(beams))

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