import sys
import os
import math
from functools import cache
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions
from my_utils import astar, flood

def parse_input():
    with open('2024/input/day20.txt','r') as input_file:
        start = 0
        end = 0
        lines = input_file.read().split("\n")
        h, w = len(lines), len(lines[0])
        racetrack = dict()
        for j,line in enumerate(lines):
            for i in range(len(line)):
                if line[i] == 'S':
                    start = i+j*1j
                if line[i] == 'E':
                    end = i+j*1j
                if line[i] == '#':
                    racetrack[i+j*1j] = 1
                else:
                    racetrack[i+j*1j] = 0
        return racetrack, start, end

@cache
def diamond(radius):
    point_cloud = []
    for i in range(-radius-1,radius+1):
        for j in range(-radius-1,radius+1):
            if abs(i)+abs(j) <= radius:
                point_cloud.append(i + j * 1j)
    return point_cloud

def part_one():
    racetrack, start, end = parse_input()
    base_path = astar(racetrack, start, end)
    base_len = len(base_path)
    shortest = flood(racetrack,end)
    cheat_histogram = dict()
    current_distance = 0
    for pos in base_path:
        for end_point in [pos+x for x in [2,-2,2j,-2j]]:
            if end_point in shortest:
                if shortest[end_point] + current_distance < base_len - 100:
                    i = base_len - (shortest[end_point] + current_distance)
                    cheat_histogram[i] = cheat_histogram.get(i, 0) + 1
        current_distance += 1
    print(sum(cheat_histogram.values()))
    

def part_two():
    racetrack, start, end = parse_input()
    base_path = astar(racetrack, start, end)
    base_len = len(base_path)
    shortest = flood(racetrack,end)
    distance_taken = flood(racetrack,start)
    distance_taken = dict(filter(lambda x:x[1] <= base_len - 100, distance_taken.items()))
    cheat_histogram = dict()
    for pos in distance_taken.keys():
        for end_point in [pos + x for x in diamond(20)]: 
            if end_point in shortest:
                d = int(abs(end_point.real - pos.real) + abs(end_point.imag - pos.imag))
                if distance_taken[pos] + shortest[end_point] + d <= base_len - 100:
                    i = base_len - distance_taken[pos] - shortest[end_point] - d
                    cheat_histogram[i] = cheat_histogram.get(i, 0) + 1
    #for k,v in dict(sorted(cheat_histogram.items())).items():
    #    print('There are {} cheats that save {} picoseconds.'.format(v,k))
    print(sum(cheat_histogram.values()))

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