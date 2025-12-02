import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions
import re

def parse_input():
    with open('2025/input/day01.txt','r') as input_file:
        steps = []
        for line in input_file.read().split('\n'):
            temp = re.match(r'(R|L)(\d+)', line)
            steps.append((temp.group(1), int(temp.group(2))))
        return steps

def part_one():
    steps = parse_input()
    current = 50
    dial_size = 100
    zero_counter = 0
    for step in steps:
        if step[0] == 'R':
            current = (current + step[1]) % dial_size
        elif step[0] == 'L':
            current = (current - step[1]) % dial_size
        if current == 0:
            zero_counter += 1
    print(zero_counter)

#answer is too low, I am missing an edge case. But I cannot figure out which
def part_two():
    steps = [('L',68),('L',30),('R',48),('L',5),('R',60),('L',55),('L',1),('L',99),('R',14),('L',82)]#parse_input()
    current = 50
    dial_size = 100
    zero_counter = 0
    for step in steps:
        if step[0] == 'R':
            q,current = divmod(current + step[1],dial_size)
            zero_counter += q
        elif step[0] == 'L':
            q,current = divmod(current - step[1],dial_size)
            zero_counter -= q
    print(zero_counter)

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