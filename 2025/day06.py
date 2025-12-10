import sys
import os
import operator
from functools import reduce

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2025/input/day06.txt','r') as input_file:
        return input_file.read().split('\n')

def part_one():
    lines = parse_input()
    problems = list(zip(*[line.split() for line in lines]))
    parsed_problems = []
    for problem in problems:
        operand = operator.add if problem[-1] == '+' else operator.mul
        parsed = list(map(int, problem[:-1])) + [operand]
        parsed_problems.append(parsed)
    grand_total = 0
    for problem in parsed_problems:
        grand_total += reduce(problem[-1], problem[:-1])
    print(grand_total)

def part_two():
    lines = parse_input()
    #making sure the last line has the correct length for zip
    lines[-1] += ' '*(len(lines[0]) - len(lines[-1]))
    columns = list(zip(*[line for line in lines]))
    problems = [[]]
    for col in columns:
        if col == tuple(' '*len(col)):
            problems.append([])
        else:
            if col[-1] != ' ':
                problems[-1].append(operator.add if col[-1] == '+' else operator.mul)
            problems[-1].append(int(''.join(col[:-1])))
    grand_total = 0
    #print(problems)
    for problem in problems:
        grand_total += reduce(problem[0], problem[1:])
    print(grand_total)

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