import sys
import re
#import util functions

def parse_input():
    with open('2024/input/day3.txt','r') as input_file:
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

if __name__ == '__main__':
    globals()[sys.argv[1]]()