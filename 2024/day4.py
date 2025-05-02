import sys
import re
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2024/input/day4.txt','r') as input_file:
        lines = input_file.readlines()
        w = len(lines[0])+5 #accounting for \n character
        h = len(lines)+6
        return w, h, ['.'*w, '.'*w, '.'*w] + ['...'+line.strip()+'...' for line in lines] + ['.'*w, '.'*w, '.'*w]

def part_one():
    width, height, data = parse_input()
    total = 0
    directions = [[(0, 0), (0, 1), (0, 2), (0, 3)], [(0, 0), (0, -1), (0, -2), (0, -3)],
                  [(0, 0), (1, 0), (2, 0), (3, 0)], [(0, 0), (-1, 0), (-2, 0), (-3, 0)],
                  [(0, 0), (1,-1), (2,-2), (3,-3)], [(0, 0), (1, 1), (2, 2), (3, 3)],
                  [(0, 0), (-1,-1), (-2,-2), (-3,-3)], [(0, 0), (-1, 1), (-2, 2), (-3, 3)]]
    for i in range(3,height-3):
        for j in range(3, width-3):
            total += [re.match(r'XMAS', x) is not None for x in [''.join([data[j + t[1]][i + t[0]] for t in d]) for d in directions]].count(True)
    print(total)

def part_two():
    width, height, data = parse_input()
    total = 0
    directions = [[(-1, -1), (0, 0), (1, 1)], [(1, -1), (0, 0), (-1, 1)]]
    for i in range(3, height - 3):
        for j in range(3, width - 3):
            if all([re.match(r'MAS|SAM', x) is not None for x in [''.join([data[j + t[1]][i + t[0]] for t in d]) for d in directions]]):
                total += 1
    print(total)

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