import sys
import os
from functools import cache
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2024/input/day21.txt','r') as input_file:
        return input_file.read().split('\n')[:-1]

def path(subsequence):
    (y,x), (Y,X) = [divmod('789456123 0A<v>'.find(t), 3) for t in subsequence]
    #construct seq
    Seq = '>' * (X - x) + 'v' * (Y - y) + '0' * (y - Y) + '<' * (x - X)
    #panic check (3,0): if so, reverse path order
    return Seq if (3,0) in [(y,X), (Y,x)] else Seq[::-1] 

@cache
def length(S, d):
    if d < 0: return len(S)+1
    return sum(length(path(subseq), d-1) for subseq in zip('A' + S, S + 'A'))

def part_one():
    codes = parse_input()
    print(sum(int(Seq[:3]) * length(Seq[:3], 2) for Seq in codes))
    length.cache_clear()


def part_two():
   codes = parse_input()
   print(sum(int(Seq[:3]) * length(Seq[:3], 25) for Seq in codes))
   length.cache_clear()

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