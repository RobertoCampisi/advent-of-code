import sys
import os
from itertools import combinations

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

empty_space = 1

def parse_input():
    with open('2023/input/day11.txt','r') as input_file:
        lines = input_file.readlines()
        galaxy_id_counter = 0
        galaxies_bse = dict() #before space expansion
        empty_row = [True]*len(lines)
        empty_col = [True]*len(lines[0])
        for j,line in enumerate(lines):
            for i,sym in enumerate(line):
                if sym == '#':
                    empty_row[j] = False
                    empty_col[i] = False
                    galaxies_bse[i+j*1j] = galaxy_id_counter
                    galaxy_id_counter += 1
        row_shift = []
        c = 0
        global empty_space
        for x in empty_row:
            if x:
                c+=empty_space
            row_shift.append(c)
        col_shift = []
        c = 0
        for x in empty_col:
            if x:
                c += empty_space
            col_shift.append(c)
        galaxies = dict()
        for g in galaxies_bse:
            i = int(g.real) + col_shift[int(g.real)]
            j = int(g.imag) + row_shift[int(g.imag)]
            galaxies[i+j*1j] = galaxies_bse[g]
        return galaxies

def part_one():
    galaxies = parse_input().keys()
    total_distance = 0
    for (g1,g2) in combinations(galaxies,2):
        #calculate manhattan distance
        total_distance += int(abs(g1.real-g2.real) + abs(g1.imag-g2.imag))
    print(total_distance)

def part_two():
    global empty_space
    empty_space = 1000000 - 1
    galaxies = parse_input().keys()
    total_distance = 0
    for (g1, g2) in combinations(galaxies, 2):
        # calculate manhattan distance
        total_distance += int(abs(g1.real - g2.real) + abs(g1.imag - g2.imag))
    print(total_distance)

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