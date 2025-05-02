import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2024/input/day2.txt','r') as input_file:
        return [list(map(int,line.strip().split(' '))) for line in input_file.readlines()]

data = parse_input()

def is_safe(report):
    diffs = [b-a for (a,b) in zip(report[:-1], report[1:])]
    first = diffs[0]
    for d in diffs[1:]:
        if 0 > first >= -3: #all negative
            if d >= 0 or d < -3:
                return False
        elif 0 < first <= 3: #all positive
            if d <= 0 or d > 3:
                return False
        else:
            return False
    return True

def is_safe_with_dampener(report):
    if is_safe(report):
        return True
    else:
        for i in range(len(report)):
            if is_safe(report[:i] + report[i+1:]):
                return True
    return False

def part_one():
    print([is_safe(line) for line in data].count(True))

def part_two():
    print([is_safe_with_dampener(line) for line in data].count(True))

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