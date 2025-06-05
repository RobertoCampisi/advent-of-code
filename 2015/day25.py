import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day25.txt','r') as input_file:
        return tuple(map(int,re.findall(r'\d+', input_file.read().strip())))

def code_index(row, col):
    n = 1
    for i in range(1,row):
        n += i
    for j in range(1,col):
        n += row+j
    return n

def generate_code(index):
    code = 20151125
    for _ in range(index-1):
        code = (code * 252533) % 33554393
    return code

def part_one():
    row, col = parse_input()
    code = generate_code(code_index(row, col))
    print(code)

def part_two():
    ...

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