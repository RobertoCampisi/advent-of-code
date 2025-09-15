import sys
import os
from collections import defaultdict
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2017/input/day03.txt','r') as input_file:
        return int(input_file.read().strip())

def part_one():
    square = parse_input()
    #find spiral radius
    sr = 1
    while square > sr * sr:
        sr += 2
    #find spiral side
    side = 4
    pos = sr*sr
    while side > 1 and square < (pos - sr + 1):
        pos -= sr + 1
        side -= 1
    #calculate distance
    middle_point = pos - (sr - 1) // 2
    dist = abs(square - middle_point)
    dist += (sr - 1) // 2
    print(dist)

def part_two():
    turn = {1:1j, 1j:-1, -1:-1j, -1j:1}
    spiral = defaultdict(lambda: 0)
    input_value = parse_input()
    #iterate spiral
    pos = 0
    d = 1
    spiral[pos] = 1
    while spiral[pos] < input_value:
        pos += d
        spiral[pos] = sum(spiral[pos+x] for x in [1, 1+1j, 1j, -1+1j, -1, -1-1j, -1j, 1-1j])
        if spiral[pos+turn[d]] == 0:
            d = turn[d]
    print(spiral[pos])

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