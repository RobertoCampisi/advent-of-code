import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2023/input/day1.txt','r') as input_file:
        return input_file.read().split('\n')

def to_int(match):
    match str:
        case 'one': return 1
        case 'two': return 2
        case 'three': return 3
        case 'four': return 4
        case 'five': return 5
        case 'six': return 6
        case 'seven': return 7
        case 'eight': return 8
        case 'nine': return 9
        case _: return int(match)

def part_one():
    lines = parse_input()
    calibration_values = [int(re.search(r'\d',l.strip())[0] + re.search(r'\d',l.strip()[::-1])[0]) for l in lines]
    print(sum(calibration_values))

def part_two():
    lines = parse_input()
    digits_pattern = re.compile(r'\d|one|two|three|four|five|six|seven|eight|nine')
    digits_pattern_r = re.compile(r'\d|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin')
    calibration_values = [to_int(re.search(digits_pattern, l.strip())[0])*10 + to_int(re.search(digits_pattern_r, l.strip()[::-1])[0]) for l in lines]
    print(sum(calibration_values))

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