import sys
import os
from collections import defaultdict
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2017/input/day08.txt','r') as input_file:
        instructions = []
        for line in input_file.read().split("\n"):
            instructions.append(line.split())
        return instructions

def condition(x, condition_operation, val):
    match condition_operation:
        case '==': return x == val
        case '>': return x > val
        case '<': return x < val
        case '<=': return x <= val
        case '>=': return x >= val
        case '!=': return x != val
        case _: return False

def part_one():
    registers = defaultdict(lambda: 0)
    for reg, op, val, _, cond_reg, cond_op, cond_val in parse_input():
        if condition(registers[cond_reg], cond_op, int(cond_val)):
            match op:
                case 'inc': registers[reg] += int(val)
                case 'dec': registers[reg] -= int(val)
    print(max(registers.values()))



def part_two():
    registers = defaultdict(lambda: 0)
    max_values_registers = defaultdict(lambda: 0)
    for reg, op, val, _, cond_reg, cond_op, cond_val in parse_input():
        if condition(registers[cond_reg], cond_op, int(cond_val)):
            match op:
                case 'inc': 
                    registers[reg] += int(val)
                    max_values_registers[reg] = max(registers[reg], max_values_registers[reg])
                case 'dec': 
                    registers[reg] -= int(val)
                    max_values_registers[reg] = max(registers[reg], max_values_registers[reg])
    print(max(max_values_registers.values()))


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