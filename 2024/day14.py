import sys
import os
import math
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

#constant
width = 101
height = 103

def parse_input():
    with open('2024/input/day14.txt','r') as input_file:
        robots = []
        for line in input_file.read().splitlines():
            pos_str ,vel_str = line.split(' ')
            pos = tuple(map(int,pos_str.split('=')[1].split(',')))
            vel = tuple(map(int,vel_str.split('=')[1].split(',')))
            robots.append({'pos':pos,'vel':vel})
        return robots

data = parse_input()

def simulate(r_init,t):
    r = r_init
    #final time step
    r_end = []
    for robot in r:
        pos_next = ((robot['pos'][0] + robot['vel'][0] * t) % width,(robot['pos'][1] + robot['vel'][1] * t) % height) 
        r_end.append({'pos':pos_next,'vel':robot['vel']})
    return r_end

def safety_factor(robots):
    #binning the robot count
    quadrants = [0,0,0,0]
    for robot in robots:
        if robot['pos'][0] < width//2:
            if robot['pos'][1] < height//2:
                quadrants[0] += 1
            elif robot['pos'][1] > height//2:
                quadrants[2] += 1
        elif robot['pos'][0] > width // 2:
            if robot['pos'][1] < height // 2:
                quadrants[1] += 1
            elif robot['pos'][1] > height // 2:
                quadrants[3] += 1
    return math.prod(quadrants)

def part_one():
    print(safety_factor(simulate(data, 100)))

def make_grid(robots, verbose=False):
    grid = [[0 for i in range(width)] for _ in range(height)]
    for robot in robots:
        grid[robot['pos'][1]][robot['pos'][0]] += 1
    if verbose:
        for k,row in enumerate(grid):
            temp = ''.join([str(i) for i in row]).replace('0','.')
            if k == math.floor(height/2):
                print(''*width)
            else:
                print(temp[:(math.floor(width/2))] + ' ' + temp[(math.floor(width/2) + 1):])
        print(''*width)
    return grid

def highest_column_count(grid):
    highest_adj_column_counts = [0]*len(grid[0])
    adjecent_column_counts = [0]*len(grid[0])
    for row in grid:
        adjecent_column_counts = [ 0 if b == 0 else a for (a,b) in zip(adjecent_column_counts, row)]
        adjecent_column_counts = [sum(x) for x in zip(adjecent_column_counts, row)]
        highest_adj_column_counts = [max(x) for x in zip(highest_adj_column_counts, adjecent_column_counts)]
    return max(highest_adj_column_counts)
        
def part_two():
    best_candidate = 0
    a = 101 
    c = 14 
    hcc = 0
    for n in range(10000):
        candidate = highest_column_count(make_grid(simulate(data, a*n + c)))
        if  candidate > hcc:
            hcc = candidate
            best_candidate = a*n+c
    print(best_candidate)
    #uncomment the next line to see a christmas tree
    #make_grid(simulate(data,best_candidate),True) 

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