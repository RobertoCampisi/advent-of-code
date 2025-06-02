import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day10.txt','r') as input_file:
        return list(map(int,input_file.read().strip()))

def elves_look_elves_say(arr):
    i = 0
    j = 1
    res = []
    while i < len(arr):
        if i == len(arr) - 1:
            res.append(j)
            res.append(arr[i])
        elif arr[i] == arr[i+1]:
            j += 1
        else:
            res.append(j)
            res.append(arr[i])
            j = 1
        i += 1
    return res

def part_one():
    seq = parse_input()
    for _ in range(40):
        seq = elves_look_elves_say(seq)
    print(len(seq))



def part_two():
    seq = parse_input()
    for _ in range(50):
        seq = elves_look_elves_say(seq)
    print(len(seq))

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