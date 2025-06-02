import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day03.txt','r') as input_file:
        directions = []
        for line in input_file.read().split('\n'):
            for symbol in line:
                match symbol:
                    case '>': directions.append(1)
                    case '<': directions.append(-1)
                    case '^': directions.append(1j)
                    case 'v': directions.append(-1j)
                    case _  : ...
        return directions

def part_one():
    directions = parse_input()
    current = 0
    visited = set([current])
    for dir in directions:
        current += dir
        visited.add(current)
    print(len(visited))


def part_two():
    directions = parse_input()
    current_santa = 0
    current_robo_santa = 0
    visited = set([current_santa])
    for i,dir in enumerate(directions):
        if i%2 == 0:
            current_santa += dir
            visited.add(current_santa)
        else:
            current_robo_santa += dir
            visited.add(current_robo_santa)
    print(len(visited))

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