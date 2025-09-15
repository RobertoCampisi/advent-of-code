import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2017/input/day05.txt','r') as input_file:
        return [int(x) for x in input_file.read().split("\n")]

def part_one():
    maze = parse_input()
    max_jumps = 100000000000
    i = 0
    for j in range(max_jumps):
        if i < len(maze):
            jump = maze[i]
            maze[i] += 1
            i += jump
        else: 
            print(j)
            break
    else:
        print("REACHED MAX JUMPS")
    

def part_two():
    maze = parse_input()
    max_jumps = 100000000000
    i = 0
    for j in range(max_jumps):
        if i < len(maze):
            jump = maze[i]
            if jump < 3:
                maze[i] += 1
            else:
                maze[i] -= 1
            i += jump
        else: 
            print(j)
            break
    else:
        print("REACHED MAX JUMPS")

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