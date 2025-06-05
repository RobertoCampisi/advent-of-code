import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day23.txt','r') as input_file:
        instructions = []
        for line in input_file.read().split('\n'):
            ws = line.replace(',','').split(' ')
            if ws[0] == 'jmp':
                instructions.append((ws[0], '', int(ws[1])))
            elif ws[0] == 'jie' or ws[0] == 'jio':
                instructions.append((ws[0], ws[1], int(ws[2])))
            else:
                instructions.append((ws[0], ws[1], 0))
        return instructions

def execute_instructions(registers, instructions):
    i = 0
    while i < len(instructions):
        op, reg, offset = instructions[i]
        match(op):
            case 'hlf': 
                registers[reg] //= 2
                i += 1
            case 'tpl': 
                registers[reg] *= 3
                i += 1
            case 'inc':
                registers[reg] += 1
                i += 1
            case 'jmp':
                i += offset
            case 'jie':
                if registers[reg] % 2 == 0:
                    i += offset
                else:
                    i += 1
            case 'jio':
                if registers[reg] == 1:
                    i += offset
                else:
                    i+= 1
    return registers

def part_one():
    instructions = parse_input()
    registers = {'a':0, 'b':0}
    registers = execute_instructions(registers, instructions)
    print(registers['b'])
            

def part_two():
    instructions = parse_input()
    registers = {'a':1, 'b':0}
    registers = execute_instructions(registers, instructions)
    print(registers['b'])

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