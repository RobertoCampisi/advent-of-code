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
            position += direction * int(ins[1:])
        elif ins.startswith('L'):
            direction *= 1j
            position += direction * int(ins[1:])
    print(abs(int(position.real)) + abs(int(position.imag)))

def on_segment(p, q, r):
    return (q.real <= max(p.real, r.real) and q.real >= min(p.real, r.real) and 
            q.imag <= max(p.imag, r.imag) and q.imag >= min(p.imag, r.imag))

def orient(p, q, r):
    val = (q.imag - p.imag) * (r.real - q.real) - \
          (q.real - p.real) * (r.imag - q.imag)
    if val == 0: return 0
    return 1 if val > 0 else 2 

def intersect(ls1, ls2):
    o1 = orient(ls1[0], ls1[1], ls2[0])
    o2 = orient(ls1[0], ls1[1], ls2[1])
    o3 = orient(ls2[0], ls2[1], ls1[0])
    o4 = orient(ls2[0], ls2[1], ls1[1])
    return o1 != o2 and o3 != o4

def part_two():
    instructions = parse_input()
    position = 0 #start
    direction = 1j #north
    visited_lines = set()
    for ins in instructions:
        if ins.startswith('R'):
            direction *= -1j
            new_position = position + direction * int(ins[1:])
        elif ins.startswith('L'):
            direction *= 1j
            new_position = position + direction * int(ins[1:])
        if any([intersect((position,new_position), l) for l in visited_lines]):
            print(visited_lines, ins ,(position, new_position))
            break
        else:
            visited_lines.add((position, new_position))
        position = new_position
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