import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions
from my_utils import astar

def parse_input():
    with open('2024/input/day18.txt','r') as input_file:
        memory = {}
        for i in range(71):
            for j in range(71):
                memory[i+j*1j] = 0
        _bytes = input_file.read().split("\n")
        for byte in _bytes[:1024]:
            x,y = map(int,byte.split(","))
            memory[x+y*1j] = 1
        return memory, _bytes[1024:]

def part_one():
    memory, _ = parse_input()    
    start = 0 + 0j
    end = 70 + 70j
    path = astar(memory, start, end)
    print(len(path))

def part_two():
    memory, remaining_bytes = parse_input()    
    start = 0 + 0j
    end = 70 + 70j
    path = astar(memory, start, end)
    for byte in remaining_bytes:
        x,y = map(int,byte.split(",")) #read byte
        memory[x+y*1j] = 1
        if x+y*1j in path: #only recalculate if the path has changed
            path = astar(memory, start, end)
        if path is None:
            print(str(x)+','+str(y))
            break

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