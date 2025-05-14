import sys
import os
from itertools import combinations

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions
def transpose(x):
    return [''.join(y) for y in zip(*x)]

def parse_input():
    with open('2023/input/day13.txt','r') as input_file:
        patterns = [pattern.split('\n') for pattern in input_file.read().split('\n\n')]
        p_arrays = []
        for p in patterns:
            p_arrays.append((pattern_to_bin_array(transpose(p)),pattern_to_bin_array(p)))
        return p_arrays

def pattern_to_bin_array(p):
    res = []
    for line in p:
        bin_str = line.replace('.','0').replace('#','1')
        res.append(int(bin_str,2))
    return res

def find_reflect(arr):
    prev = -1
    for i,n in enumerate(arr):
        if n == prev:
            j = 1
            while 0 <= i - j and i + j - 1 < len(arr):
                if arr[i - j] != arr[i + j - 1]:
                    break
                j += 1
            if i - j < 0 or i + j - 1 == len(arr):
                return i+1
        prev = n
    return -1

def part_one():
    patterns = parse_input()
    print(sum(find_reflect(p1) + find_reflect(p2) * 100 for p1,p2 in patterns))

def part_two():
    patterns = parse_input()[0:4]
    res = 0
    for p1,p2 in patterns:
        #find candidates for potential smudges
        old_relection = [find_reflect(p1),find_reflect(p2)]
        candidates = dict()
        for a,b in combinations(range(0,len(p1)),2):
            candidates[(a,b)] = abs(p1[a]-p1[b]).bit_count() == 1
        candidates2 = dict()
        for a,b in combinations(range(0,len(p2)),2):
            candidates2[(a,b)] = abs(p2[a]-p2[b]).bit_count() == 1
        #find new relection
        def smudge_reflect(_candidates,_p):
            _res = []
            for smudge in [k for k, v in _candidates.items() if v]:
                s1, s2 = smudge
                smudged1 = _p.copy()
                smudged1[s1] = _p[s2]
                smudged2 = _p.copy()
                smudged2[s2] = _p[s1]
                smudges_res = [find_reflect(smudged1),find_reflect(smudged2)]
                for sr in smudges_res:
                    if sr not in old_relection or sr != -1:
                        _res.append(sr)
            return _res
        print(smudge_reflect(candidates,p1))
        print(smudge_reflect(candidates2,p2))
        #found multiple smudge reflections, this is probably due to a misunderstanding of the puzzle.

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