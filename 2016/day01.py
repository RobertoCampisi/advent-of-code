import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2016/input/day01.txt','r') as input_file:
        return [d.strip() for d in input_file.read().strip().split(',')]

def part_one():
    instructions = parse_input()
    position = 0 #start
    direction = 1j #north
    for ins in instructions:
        if ins.startswith('R'):
            direction *= -1j
        elif ins.startswith('L'):
            direction *= 1j
        position += direction * int(ins[1:])
    print(abs(int(position.real)) + abs(int(position.imag)))

def part_two():
    instructions = parse_input()
    position = 0 #start
    direction = 1j #north
    visited = set()
    found_duplicate = False
    for ins in instructions:
        if ins.startswith('R'):
            direction *= -1j
        elif ins.startswith('L'):
            direction *= 1j
        for x in range(int(ins[1:])):
            position += direction
            if position in visited:
                found_duplicate = True
                break
            visited.add(position)
        if found_duplicate: break
    print(abs(int(position.real)) + abs(int(position.imag)))

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