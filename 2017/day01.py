import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2017/input/day01.txt','r') as input_file:
        return input_file.read().strip() 
def part_one():
    captcha = parse_input()
    matches = re.finditer(r'(?=(\d)\1)', captcha + captcha[0])# re-add first digit to the end 
    print(sum([int(match.group(1)) for match in matches]))

def part_two():
    captcha = parse_input()
    n = len(captcha) // 2
    matches = re.finditer(fr'(\d)(?=.{{{n-1}}}\1)', captcha+captcha[:n])# re-add first digit to the end 
    print(sum([int(match.group(1)) for match in matches]))

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