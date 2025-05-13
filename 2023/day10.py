import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2023/input/day10.txt','r') as input_file:
        pipes = dict()
        start = 0
        lines = input_file.read().split('\n')
        width, height = len(lines[0]), len(lines)
        for j,line in enumerate(lines):
            for i, symbol in enumerate(line):
                pipes[i+j*1j] = symbol
                if symbol == 'S':
                    start = i+j*1j
        return pipes, start, width, height

def verify_connection(grid, cases, positions):
    res = []
    for i, c in enumerate(cases):
        if positions[i] in grid and grid[positions[i]] in c:
            res.append(positions[i])
    return res

def get_neighbors(grid, pos):
    match grid[pos]:
        case '|': return verify_connection(grid, ['|7F','|LJ'],[pos-1j, pos+1j])
        case '-': return verify_connection(grid,['-LF','-7J'],[pos-1, pos+1])
        case 'L': return verify_connection(grid,['|7F','-7J'],[pos-1j, pos+1])
        case 'J': return verify_connection(grid,['-LF','|7F'],[pos-1, pos-1j])
        case '7': return verify_connection(grid,['-LF','|LJ'],[pos-1, pos+1j])
        case 'F': return verify_connection(grid,['-7J','|LJ'],[pos+1, pos+1j])
        case 'S': return verify_connection(grid,['-LF','-7J','|7F','|LJ'],[pos-1, pos+1, pos-1j, pos+1j])
        case _: return []
    #return list(filter(lambda x: x in grid and grid[x] != 1, [pos+1,pos-1,pos+1j,pos-1j]))
  

def part_one():
    pipes, start, _ , _ = parse_input()
    iteration_set = set(get_neighbors(pipes, start)) #flood both ways
    distances = {start: 0}
    next_set = set()
    current_distance = 1
    while iteration_set:
        while iteration_set:
            current_pos = iteration_set.pop()
            if current_pos not in distances:
                distances[current_pos] = current_distance
                for e in get_neighbors(pipes, current_pos):
                    next_set.add(e)
        iteration_set = next_set
        next_set = set()
        current_distance += 1
    print(max(distances.values()))

def part_two():
    pipes, start, width, height = parse_input()
    iteration_set = set(get_neighbors(pipes, start)[1:]) #make sure the flood only goes into one direction
    loop = []
    next_set = set()
    while iteration_set:
        while iteration_set:
            current_pos = iteration_set.pop()
            if current_pos not in loop:
                loop.append(current_pos)
                for e in get_neighbors(pipes, current_pos):
                    next_set.add(e)
        iteration_set = next_set
        next_set = set()
    #calculate Area using the shoelace theorem
    total_area = 0
    for i in range(0,len(loop)):
        a, b = int(loop[i].real), int(loop[i].imag)
        c, d = int(loop[(i+1)%len(loop)].real), int(loop[(i+1)%len(loop)].imag)
        total_area += (a*d-b*c) #determinant
    total_area = abs(total_area) // 2
    #applying Pick theorem to calculate the inner points
    inner = total_area + 1 - len(loop)//2
    print(inner)
    #for j in range(0, height):
    #   print(''.join([pipes[i+j*1j] if (i+j*1j) not in inside else 'I' for i in range(0, width)]))
    #   print(''.join(['I' if row_part[i + j * 1j] else '.' for i in range(0, width)]))


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