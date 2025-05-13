import sys
import os
from functools import cache
from collections import defaultdict
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

def total_arrangements(_string,code):
    def is_valid(_id, _amount): #helper function
        return _id == len(code) or _id == len(code) - 1 and _amount == code[_id]
    perms = defaultdict(int)
    perms[(0,0)] = 1 #(_id, _amount)
    for sym in _string:
        next_it = []
        for key, perm_count in perms.items():
            _id, _amount = key
            if sym != '#':
                if _amount == 0:
                    next_it.append((_id,_amount,perm_count))
                elif _amount == code[_id]:
                    next_it.append((_id+1,0,perm_count))
            if sym != '.':
                if _id < len(code) and _amount < code[_id]:
                    next_it.append((_id,_amount + 1, perm_count))
        perms.clear()
        for _id, _amount, perm_count in next_it:
            perms[(_id,_amount)] += perm_count
    return sum(a for k,a in perms.items() if is_valid(*k))

def part_one():
    data = parse_input()
    print(sum([total_arrangements(ar_string,code) for ar_string, code in data]))

def part_two():
    data = parse_input()
    print(sum([total_arrangements('?'.join([ar_string]*5), tuple(list(code)*5)) for ar_string, code in data]))

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