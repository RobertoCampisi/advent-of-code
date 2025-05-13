import sys
import os
from functools import cache
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2023/input/day12.txt','r') as input_file:
        lines = input_file.readlines()
        data = []
        for l in lines:
            arrng_str, code = l.split(' ')
            data.append((arrng_str, tuple([int(c) for c in code.split(',')])))
    return data

@cache
def valid(arrangement, code):
    if not code:
        return '#' not in arrangement
    last = code[-1]
    if len(code) == 1 & len(arrangement) > last:
        return False
    k = 0
    c = 0
    for sym in arrangement[::-1]:
        k-=1
        if sym == '#':
            c += 1
        elif sym == '.' and c > 0:
            if c != last:
                return False
            else:
                break
        elif sym != '.':
            return False
    if c == 0:
        return False
    if len(code) == 1 and c != last:
        return False
    return valid(arrangement[:k],code[:-1])


def total_arrangements(ar_string,code):
    print(ar_string, code)
    res = 0
    if '?' not in ar_string:
        if valid(ar_string, code):
            print('Valid')
            res += 1
    else:
        for i in range(len(ar_string)):
            if ar_string[i] == '?' and i < len(ar_string) - 1:
                res += total_arrangements(ar_string[:i] + '.' + ar_string[i+1:], code)
                res += total_arrangements(ar_string[:i] + '#' + ar_string[i+1:], code)
                break
            elif ar_string[i] == '?':
                res += total_arrangements(ar_string[:i] + '.', code)
                res += total_arrangements(ar_string[:i] + '#', code)
                break
    return res

def part_one():
    data = parse_input()
    print(sum([total_arrangements(ar_string,code) for ar_string, code in data]))

def part_two():
    data = parse_input()[:1]
    print(sum([total_arrangements(ar_string*5, tuple(list(code)*5)) for ar_string, code in data]))

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