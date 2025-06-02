import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day08.txt','r') as input_file:
        return input_file.read().split('\n')

def part_one():
    literal_strings = parse_input()
    lit_str_cha_count = 0
    mem_cha_count = 0
    for literal_string in literal_strings:
        lit_str_cha_count += len(literal_string)
        quotes = 2
        escaped = len(re.findall(r'\\\\|\\"', literal_string))
        escaped += 3 * len(re.findall(r'\\x[\da-f]{2}',literal_string))
        mem_cha_count += len(literal_string) - quotes - escaped
    print(lit_str_cha_count - mem_cha_count)


def part_two():
    literal_strings = parse_input()
    lit_str_cha_count = 0
    mem_cha_count = 0
    for literal_string in literal_strings:
        mem_cha_count += len(literal_string)
        quotes = 2
        escaped = len(re.findall(r'\\|"', literal_string))
        lit_str_cha_count += len(literal_string) + quotes + escaped
    print(lit_str_cha_count - mem_cha_count)

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