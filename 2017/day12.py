
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2017/input/day12.txt','r') as input_file:
        graph = dict()
        for line in input_file.read().split('\n'):
            line = line.replace(',','')
            ws = line.split()
            node = ws[0]
            neighbours = ws[2:]
            graph[node] = neighbours
        return graph

def part_one():
    pipe_system = parse_input()
    seen = set() 
    node_queue = ['0']
    while node_queue:
        current = node_queue.pop(0)
        if current not in seen:
            seen.add(current)
            nbrs = pipe_system[current]
            node_queue.extend(nbrs)
    print(len(seen))

def part_two():
    pipe_system = parse_input()
    groups = []
    total_seen = set()
    for i in range(2000):
        node = str(i)
        if node not in total_seen:
            seen = set()
            node_queue = [node] 
            while node_queue:
                current = node_queue.pop(0)
                if current not in seen:
                    seen.add(current)
                    total_seen.add(current)
                    nbrs = pipe_system[current]
                    node_queue.extend(nbrs)
            groups.append(seen)
    print(len(groups))

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