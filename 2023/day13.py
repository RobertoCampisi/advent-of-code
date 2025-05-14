import sys
import os
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
    ...

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