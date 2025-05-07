import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2024/input/day10.txt','r') as input_file:
        lines = input_file.read().strip().split("\n")
        w = len(lines[0]) + 2
        for i, line in enumerate(lines):
            lines[i] = '.' + line + '.'
        return ['.' * w] + lines + ['.' * w]

def score_trailhead(grid, x, y, dir, allow_duplicates):
    if grid[y][x] != str(0):
            return 0
    paths = set()
    paths.add((x,y))
    for k in range(1,10):
        next_paths = []
        for p in paths:
            for d in dir:
                if grid[p[1]+d[1]][p[0]+d[0]] == str(k):
                    value = (p[0]+d[0],p[1]+d[1])
                    #part 1 does not allow for duplicate paths, part 2 does
                    if allow_duplicates or value not in next_paths:
                        next_paths.append(value)
        if len(next_paths) == 0:
            break
        paths = next_paths
        #print(len(next_paths), next_paths)
    return len(paths)

def part_one():
    grid = parse_input()
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    trailheads_row_starts = ((re.finditer(r'0', line), i) for i, line in enumerate(grid))
    total_score = 0
    for th_r in trailheads_row_starts:
        row, y1 = th_r
        for th in row:
            total_score += score_trailhead(grid, th.span()[0], y1, directions, False)
    print(total_score)

def part_two():
    grid = parse_input()
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    trailheads_row_starts = ((re.finditer(r'0', line), i) for i, line in enumerate(grid))
    total_score = 0
    for th_r in trailheads_row_starts:
        row, y1 = th_r
        for th in row:
            total_score += score_trailhead(grid, th.span()[0], y1, directions, True)
    print(total_score)

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