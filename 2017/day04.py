import sys
import os
from itertools import permutations
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2017/input/day04.txt','r') as input_file:
        return [[word for word in line.split()] for line in input_file.read().split("\n")]


def valid_passphrase(pssphrs):
    seen = set()
    for w in pssphrs:
        if w in seen:
            return False
        else:
            seen.add(w)
    return True

def part_one():
    passphrases = parse_input()
    valid_counter = 0
    for passphrase in passphrases:
        valid_counter += valid_passphrase(passphrase)
    print(valid_counter)    
        
def valid_passphrase_strong(pssphrs):
    seen = set()
    for w in pssphrs:
        if w in seen:
            return False
        else:
            for comb in permutations(w,len(w)):
                seen.add(''.join(comb))
    return True        

def part_two():
    passphrases = parse_input()
    valid_counter = 0
    for passphrase in passphrases:
        valid_counter += valid_passphrase_strong(passphrase)
    print(valid_counter)    

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