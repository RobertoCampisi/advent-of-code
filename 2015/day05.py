import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day05.txt','r') as input_file:
        return input_file.read().split('\n')

def is_nice(word):
    return (
        re.search(r'.*([aeiou].*){3}', word) 
        and re.search(r'(.)\1', word) 
        and not re.search(r'(ab|cd|pq|xy)', word)
    )

def is_nice2(word):
    return (
        re.search(r'(..).*\1',word)
        and re.search(r'(.).\1',word)
    )

def part_one():
    words = parse_input()
    nice_count = 0
    for w in words:
        if is_nice(w):
            nice_count += 1
    print(nice_count)

def part_two():
    words = parse_input()
    nice_count = 0
    for w in words:
        if is_nice2(w):
            nice_count += 1
    print(nice_count)

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