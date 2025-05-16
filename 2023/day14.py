import sys
import os
from copy import deepcopy
from collections import defaultdict
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2023/input/day14.txt','r') as input_file:
        #grid = [list(l) for l in input_file.read().split('\n')]
        lines = input_file.read().split('\n')
        width, height = len(lines[0]), len(lines)
        round_rocks = defaultdict(bool)
        square_rocks = defaultdict(bool)
        for y,l in enumerate(lines):
            for x,sym in enumerate(l):
                if sym == '#': square_rocks[(x,y)] = True
                elif sym == 'O': round_rocks[(x,y)] = True  
        return round_rocks,square_rocks,width,height

def fall_north(round_rocks,square_rocks,w,h):
    fall_pos = [0] * w #state where the rock will fall to
    for y in range(h):
        for x in range(w):
            if square_rocks[(x,y)]:
                fall_pos[x] = y + 1
            if round_rocks[(x,y)]:
                round_rocks[(x,y)] = False
                round_rocks[(x,fall_pos[x])] = True
                fall_pos[x] += 1
    return round_rocks

def fall_west(round_rocks,square_rocks,w,h):
    fall_pos = [0] * h #state where the rock will fall to
    for y in range(h):
        for x in range(w):
            if square_rocks[(x,y)]:
                fall_pos[y] = x + 1
            if round_rocks[(x,y)]:
                round_rocks[(x,y)] = False
                round_rocks[(fall_pos[y],y)] = True
                fall_pos[y] += 1
    return round_rocks

def fall_south(round_rocks,square_rocks,w,h):
    fall_pos = [h-1] * w #state where the rock will fall to
    for y in range(h)[::-1]:
        for x in range(w):
            if square_rocks[(x,y)]:
                fall_pos[x] = y - 1
            if round_rocks[(x,y)]:
                round_rocks[(x,y)] = False
                round_rocks[(x,fall_pos[x])] = True
                fall_pos[x] -= 1
    return round_rocks

def fall_east(round_rocks,square_rocks,w,h):
    fall_pos = [w-1] * h #state where the rock will fall to
    for y in range(h):
        for x in range(w)[::-1]:
            if square_rocks[(x,y)]:
                fall_pos[y] = x - 1
            if round_rocks[(x,y)]:
                round_rocks[(x,y)] = False
                round_rocks[(fall_pos[y],y)] = True
                fall_pos[y] -= 1
    return round_rocks

#too expensive too use
def rotate(grid):
    return list(map(list, zip(*grid[::-1])))

def part_one():
    r_rocks, sq_rocks, width, height = parse_input()
    r_rocks = fall_north(r_rocks, sq_rocks, width, height)
    total_weight = 0
    for (x,y), v in r_rocks.items():
        total_weight += (height - y) * v
    print(total_weight)
    
def part_two():
    r_rocks, sq_rocks, width, height = parse_input()
    #prev = deepcopy(r_rocks)
    for _ in range(1000000000):
        r_rocks = fall_north(r_rocks, sq_rocks, width, height)
        r_rocks = fall_west(r_rocks, sq_rocks, width, height)
        r_rocks = fall_south(r_rocks, sq_rocks, width, height)
        r_rocks = fall_east(r_rocks, sq_rocks, width, height)
        #if r_rocks == prev:
        #    print("SHORTCUT FOUND")
        #    break
        #prev = deepcopy(r_rocks)
    total_weight = 0
    for (x,y), v in r_rocks.items():
        total_weight += (height - y) * v
    print(total_weight)
        

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