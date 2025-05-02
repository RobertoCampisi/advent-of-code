import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2024/input/day12.txt','r') as input_file:
        #using pythons j imaginary numbers for the index
        grid = {i+j*1j: c for i,row in enumerate(input_file)
            for j,c in enumerate(row.strip())}
        
        #each point belongs to a set                  
        sets = {p: {p} for p in grid}
        return grid, sets

#computes the regions
def find_regions(grid, sets):
    for p in grid:
        for n in p+1, p-1, p+1j, p-1j:
            if n in grid and grid[p] == grid[n]:
                #expand region set of each point
                sets[p] |= sets[n]
                for x in sets[p]: 
                    sets[x] = sets[p]
    #filter unique sets
    sets = {tuple(s) for s in sets.values()}
    return sets

def part_one():
    def edge(ps):
        P = {(p,d) for d in (+1,-1,+1j,-1j) for p in ps if p+d not in ps}
        return P
    sets = find_regions(*parse_input())
    #compute price of the fence
    print(sum(len(s) * len(edge(s)) for s in sets))

def part_two():
    def edge(ps):
        P = {(p,d) for d in (+1,-1,+1j,-1j) for p in ps if p+d not in ps}
        return P - {(p+d*1j, d) for p,d in P}
    sets = find_regions(*parse_input())
    #compute price of the fence
    print(sum(len(s) * len(edge(s)) for s in sets))

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