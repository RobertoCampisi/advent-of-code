import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions
import re

def parse_input():
    with open('2025/input/day02.txt','r') as input_file:
        ranges = []
        for r in input_file.read().split(','):
            rs = r.split('-')
            ranges.append((int(rs[0]),int(rs[1])))
        return ranges

def part_one():
    ranges = parse_input()
    invalid_id_sum = 0
    for rng in ranges:
        cur = rng[0]
        while cur <= rng[1]:
            cur_str = str(cur)
            x = len(cur_str)
            if x % 2 == 0:
                if cur_str[:x//2] == cur_str[x//2:]:
                    invalid_id_sum += cur
            cur += 1
    print(invalid_id_sum)

def part_two():
    ranges = parse_input()
    invalid_id_sum = 0
    for rng in ranges:
        cur = rng[0]
        while cur <= rng[1]:
            cur_str = str(cur)
            if re.fullmatch(r'(\d+)\1+',cur_str):
                invalid_id_sum += cur
            cur += 1
    print(invalid_id_sum)

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