import sys
import os
from functools import cache, reduce
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2016/input/day02.txt','r') as input_file:
        return [x.strip() for x in input_file.read().split('\n')]

ins_dict = {'U': -1j, 'D': 1j, 'R': 1, 'L': -1}

@cache
def next_position_one(pos, instruction):
    pos_real = min(2,max(0,pos.real + ins_dict[instruction].real))
    pos_imag = min(2,max(0,pos.imag + ins_dict[instruction].imag))
    return complex(pos_real, pos_imag)

@cache
def next_position_two(pos, instruction):
    new_pos = pos + ins_dict[instruction]
    distance_from_center = abs(new_pos.real - 2) + abs(new_pos.imag - 2)
    if distance_from_center > 2:
        return pos
    return new_pos

def part_one():
    complete_instructions = parse_input()
    pos = complex(1, 1)
    code = ''
    for instructions in complete_instructions:
        pos = reduce(next_position_one, instructions, pos)
        code += '123456789'[int(pos.real + pos.imag * 3)]
    print(code)

def part_two():
    complete_instructions = parse_input()
    pos = complex(0, 2)
    code = ''
    for instructions in complete_instructions:
        pos = reduce(next_position_two, instructions, pos)
        code += '..1...234.56789.ABC...D..'[int(pos.real + pos.imag * 5)]
    print(code)

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