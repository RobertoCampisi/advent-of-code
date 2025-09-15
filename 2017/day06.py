import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2017/input/day06.txt','r') as input_file:
        return [int(n) for n in input_file.read().split()]

def part_one():
    mem_banks = parse_input()
    max_count = 100000
    seen = dict()
    for i in range(max_count):
        if not tuple(mem_banks) in seen.keys():
            seen[tuple(mem_banks)] = i
            index = max(reversed(range(len(mem_banks))), key=lambda x: mem_banks[x])
            blocks, mem_banks[index] = mem_banks[index], 0
            while blocks > 0:
                index = (index + 1) % len(mem_banks)
                mem_banks[index] += 1
                blocks -= 1
        else:
            print(seen[tuple(mem_banks)])
            break

    

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