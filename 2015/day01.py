import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day01.txt','r') as input_file:
        return input_file.readlines()[0].strip()

def part_one():
    floor = 0
    directions = parse_input()
    for symbol in directions:
        match symbol:
            case '(': floor += 1
            case ')': floor -= 1
            case _: ...
    print(floor)

def part_two():
    floor = 0
    directions = parse_input()
    for i, symbol in enumerate(directions):
        match symbol:
            case '(': floor += 1
            case ')': floor -= 1
            case _: ...
        if floor == -1:
            print(i+1)
            break
    

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