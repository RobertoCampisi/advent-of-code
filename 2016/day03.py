import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2016/input/day03.txt','r') as input_file:
        shapes = []
        for line in input_file.read().split('\n'):
            shapes.append([int(side.strip()) for side in line.split()])
        return shapes

def is_possible_triangle(a,b,c):
    return a + b > c and b + c > a and c + a > b

def part_one():
    potential_triangles = parse_input()
    possible_count = 0
    for pt in potential_triangles:
        if is_possible_triangle(*pt):
            possible_count += 1
    print(possible_count)


def part_two():
    potential_triangles = parse_input()
    possible_count = 0
    i = 0
    while i * 3 < len(potential_triangles):
        #restructure: take 3 potential_triangles and regroup them by columns
        triangles = [[potential_triangles[i*3][j],potential_triangles[i*3+1][j],potential_triangles[i*3+2][j]] for j in [0,1,2]]
        possible_count += sum([is_possible_triangle(*t) for t in triangles])
        i += 1
    print(possible_count)

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