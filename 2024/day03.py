import sys
import re
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2024/input/day03.txt','r') as input_file:
        return input_file.readlines()

data = parse_input()

def part_one():
    total = 0
    for line in parse_input():
        uncorrupted = re.findall(r'mul\([0-9]+,[0-9]+\)|do\(\)|don\'t\(\)', line.strip())
        for operation in uncorrupted:
            op = re.findall(r'(\w+)\((\S*)\)', operation)[0]
            if op[0] == 'mul':
                operands = op[1].split(',')
                total += int(operands[0]) * int(operands[1])
    print(total)

def part_two():
    total = 0
    enabled = True
    for line in parse_input():
        uncorrupted = re.findall(r'mul\([0-9]+,[0-9]+\)|do\(\)|don\'t\(\)', line.strip())
        for operation in uncorrupted:
            op = re.findall(r'(\w+)\((\S*)\)', operation)[0]
            if op[0] == 'mul':
                if enabled:
                    operands = op[1].split(',')
                    total += int(operands[0]) * int(operands[1])
            elif op[0] == 'do':
                enabled = True
            elif op[0] == 't':
                enabled = False
    print(total)

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