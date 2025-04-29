import sys
#import util functions

def parse_input():
    with open('2024/input/day5.txt','r') as input_file:
        return ...

data = parse_input()

def part_one():
    ...

def part_two():
    ...

def benchmark(func, n):
    from time import time_ns
    start = time_ns() // 1_000_000
    sys.stdout = None  # bit hacky but it works
    for i in range(0, int(n)):
        globals()[func]()
    sys.stdout = sys.__stdout__ #restore
    end = time_ns() // 1_000_000
    print((end - start) / int(n), end='')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        globals()[sys.argv[1]]()
    elif len(sys.argv) > 2:
        globals()[sys.argv[1]](*sys.argv[2:])
    else:
        raise RuntimeError