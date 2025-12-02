import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2017/input/day15.txt','r') as input_file:
        return [int(line.split()[-1]) for line in input_file.read().split('\n')]

def gen_next(a, b):
    next_a = (a * 16807) % 2147483647
    next_b = (b * 48271) % 2147483647
    #judge compair
    judge_verdict = 0
    if (next_a & 65535) == (next_b & 65535):
        judge_verdict = 1
    return next_a, next_b, judge_verdict

def part_one():
    a,b = parse_input()
    judge_count = 0
    for _ in range(40_000_000):
        a,b, judge_verdict = gen_next(a,b)
        judge_count += judge_verdict
    print(judge_count)
    
def gen_next_improved(a, b):
    next_a = (a * 16807) % 2147483647
    while next_a % 4 != 0:
        next_a = (next_a * 16807) % 2147483647
    next_b = (b * 48271) % 2147483647
    while next_b % 8 != 0:
        next_b = (next_b * 48271) % 2147483647
    #judge compair
    judge_verdict = 0
    if (next_a & 65535) == (next_b & 65535):
        judge_verdict = 1
    return next_a, next_b, judge_verdict

def part_two():
    a,b = parse_input()
    judge_count = 0
    for _ in range(5_000_000):
        a,b, judge_verdict = gen_next_improved(a,b)
        judge_count += judge_verdict
    print(judge_count)

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