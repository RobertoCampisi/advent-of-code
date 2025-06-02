import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day02.txt','r') as input_file:
        box_dimensions = []
        for line in input_file.read().split('\n'):
            l, w, h = line.split('x')
            box_dimensions.append((int(l),int(w),int(h)))
        return box_dimensions

def part_one():
    boxes = parse_input()
    sqf_wrapping_paper = 0
    for box in boxes:
        sides = [box[0] * box[1], box[1] * box[2], box[2] * box[0]]
        sqf_wrapping_paper += 2*sum(sides) + min(sides)
    print(sqf_wrapping_paper)

def part_two():
    boxes = parse_input()
    sqf_ribbon = 0
    for box in boxes:
        perimeter  = [2 * box[0] + 2 * box[1], 2 * box[1] + 2 * box[2], 2 * box[2] + 2 * box[0]]
        sqf_ribbon += min(perimeter) + box[0] * box[1] * box[2]
    print(sqf_ribbon)

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