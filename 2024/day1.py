import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import util functions

def parse_input():
    with open('2024/input/day1.txt','r') as input_file:
        return input_file.readlines()

data = parse_input()

def part_one():

    left, right = [], []
    for line in data:
        l, r = list(map(int, line.split("   ")))
        left.append(l)
        right.append(r)
    print(sum([abs(a - b) for (a,b) in zip(sorted(left),sorted(right))]))


def part_two():
    left, right = [], {}
    for line in data:
        l, r = list(map(int, line.split("   ")))
        left.append(l)
        right[r] = right.get(r,0) + 1
    print(sum([a * right.get(a,0) for a in left]))

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