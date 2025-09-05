import sys
import os
import re
from collections import defaultdict
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2016/input/day08.txt','r') as input_file:
        instructions = []
        for line in input_file.read().split('\n'):
            words = line.split(' ')
            if words[0] == 'rect':
                arguments = re.findall(r'\d+?',words[1])
                instructions.append((words[0], int(arguments[0]), int(arguments[1])))
            elif words[0] == 'rotate':
                argument1 = re.search(r'\d+', words[2])
                argument2 = re.search(r'\d+', words[4])
                instructions.append((words[1], int(argument1[0]), int(argument2[0])))
        return instructions

class Grid:
    def __init__(self, _width, _height):
        self.width = _width
        self.height = _height
        self.grid = defaultdict(lambda: False)
    
    def rect(self, rect_width, rect_height):
        for j in range(min(rect_height, self.height)):
            for i in range(min(rect_width, self.width)):
                self.grid[i+j*1j] = True
    
    def rotate_row(self, idx, shift):
        temp_row = []
        for i in range(self.width):
            temp_row.append(self.grid[((i - shift) % self.width) + idx * 1j])
        for i,v in enumerate(temp_row):
            self.grid[i + idx * 1j] = v

    def rotate_column(self, idx, shift):
        temp_col = []
        for j in range(self.height):
            temp_col.append(self.grid[idx + ((j - shift) % self.height) * 1j])
        for j,v in enumerate(temp_col):
            self.grid[idx + j * 1j] = v
    
    def __str__(self):
        res = ""
        for j in range(self.height):
            res += ''.join(['#' if self.grid[i + j * 1j] else '.' for i in range(self.width)]) + "\n"
        return res
    
    def pixels_lit(self):
        return sum(self.grid.values())

def part_one():
    instructions = parse_input()
    screen = Grid(50, 6) 
    for ins in instructions:
        match ins[0]:
            case 'rect': 
                screen.rect(ins[1], ins[2])
            case 'row': 
                screen.rotate_row(ins[1], ins[2])
            case 'column': 
                screen.rotate_column(ins[1], ins[2])
        #debug statements
        print(ins) 
        print(screen)
        print(screen.pixels_lit()) 
    print(screen.pixels_lit())

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