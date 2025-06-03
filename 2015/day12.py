import sys
import os
import re
import json
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day12.txt','r') as input_file:
        return input_file.read().strip()

def sum_no_red(node):
    res = 0
    if isinstance(node, dict):
        for k,v in node.items():
            if v == 'red':
                return 0
            elif isinstance(v, dict) or isinstance(v, list):
                res += sum_no_red(v)
            elif isinstance(v, int):
                res += v
    elif isinstance(node, list):
        for e in node:
            if isinstance(e, int):
                res += e
            elif isinstance(e, dict) or isinstance(e, list):
                res += sum_no_red(e)
    return res


def part_one():
    print(sum(map(int,re.findall(r'-*\d+',parse_input()))))

def part_two():
    root = json.loads(parse_input())
    print(sum_no_red(root))


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