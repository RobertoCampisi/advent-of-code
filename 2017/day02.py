import sys
import os
from itertools import combinations
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2017/input/day02.txt','r') as input_file:
        return [[int(d) for d in line.split()] for line in input_file.read().split("\n")]

def part_one():
    spreadsheet = parse_input()
    print(sum([max(row) - min(row) for row in spreadsheet]))

def part_two():
    spreadsheet = parse_input()
    total_sum = 0
    for row in spreadsheet:
        for a,b in combinations(row,2):
            d1 = divmod(a,b)
            d2 = divmod(b,a)
            if d1[0]>0 and d1[1]==0:
                total_sum += d1[0]
                break
            if d2[0]>0 and d2[1]==0:
                total_sum += d2[0]
                break
    print(total_sum)

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