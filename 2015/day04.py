import sys
import os
from hashlib import md5
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day04.txt','r') as input_file:
        return input_file.read().split('\n')[0]

def part_one():
    secret_key = parse_input()
    number = 1
    while not (md5((secret_key + str(number)).encode()).hexdigest()).startswith('00000'):
        number += 1
    print(number)

def part_two():
    secret_key = parse_input()
    number = 1
    while not (md5((secret_key + str(number)).encode()).hexdigest()).startswith('000000'):
        number += 1
    print(number)

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