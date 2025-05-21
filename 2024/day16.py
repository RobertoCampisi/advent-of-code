import sys
import os
from collections import defaultdict
from math import inf
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2024/input/day16.txt','r') as input_file:
        input_data = input_file.read().split('\n')
        maze = defaultdict(lambda:1)
        w, h = len(input_data[0]), len(input_data)
        for j,row in enumerate(input_data):
            for i,ch in enumerate(list(row)):
                maze[i+j*1j] = 1 if ch == '#' else 0
        return maze, w, h
  
def part_one():
    maze, w, h = parse_input()
    start = 1+(h-2)*1j
    end = (w-2)+1j

    edges = []
    nodes = set()
    visited = set()

    nodes.add((start,1))
    visited.add(start)

    def prance(grid, start, d):
        perpendicular = {1:(-1j,1j),-1:(1j,-1j),1j:(1,-1),-1j:(-1,1)}
        counter = 0
        queue = [(start,d)]
        while len(queue) > 0:
            pos, old_d = queue.pop(0) 
            for d in [1,-1,1j,-1j]:
                i = 1
                while (grid[pos + d*i] != 1 and all((grid[pos+d*(i-1)+p] == 1 or i == 1 for p in perpendicular[d]))) and (pos + d*i,d) not in visited:
                    visited.add((pos+d*i,d))
                    i += 1
                if i > 1:
                    if old_d != d:
                        nodes.add((pos,d))
                        edges.append(((pos,old_d),(pos,d),1000))
                    nodes.add((pos+d*(i-1),d))
                    edges.append(((pos,d),(pos+d*(i-1),d),(i-1)))
                    queue.append((pos+d*(i-1),d))
                    for d2 in [1,-1,1j,-1j]:
                            if d2 != d:
                                if (pos+d*(i-1), d2) in visited:
                                    edges.append(((pos+d*(i-1),d),(pos+d*(i-1),d2),1000))
    #create graph
    prance(maze,start,1)  
    #Dijkstra algorithm  
    previous = {n: None for n in nodes}
    distance = {n: inf for n in nodes}
    distance[(start,1)] = 0
    queue = nodes
    while len(queue) > 0:
        min_dist = inf
        min_cand = None
        for k in queue:
            if distance[k] < min_dist:
                min_dist = distance[k]
                min_cand = k
        if min_cand is not None:
            queue.remove(min_cand)
            for u in filter(lambda x: x[0] == min_cand, edges):
                alt = distance[min_cand] + u[2]
                if alt < distance[u[1]]:
                    distance[u[1]] = alt
                    previous[u[1]] = min_cand
    end_distances = [distance[(end,d)] if (end,d) in distance else inf for d in [1,-1,1j,-1j]]
    print(min(end_distances))

    #path = [previous[(end,-1j)]]
    #while path[-1] != (start,1):
    #    path.append(previous[path[-1]])

def part_two():
    maze, w, h = parse_input()
    start = 1+(h-2)*1j
    end = (w-2)+1j

    edges = []
    nodes = set()
    visited = set()

    nodes.add((start,1))
    visited.add(start)

    def prance(grid, start, d):
        perpendicular = {1:(-1j,1j),-1:(1j,-1j),1j:(1,-1),-1j:(-1,1)}
        counter = 0
        queue = [(start,d)]
        while len(queue) > 0:
            pos, old_d = queue.pop(0) 
            for d in [1,-1,1j,-1j]:
                i = 1
                while (grid[pos + d*i] != 1 and all((grid[pos+d*(i-1)+p] == 1 or i == 1 for p in perpendicular[d]))) and (pos + d*i,d) not in visited:
                    visited.add((pos+d*i,d))
                    i += 1
                if i > 1:
                    if old_d != d:
                        nodes.add((pos,d))
                        edges.append(((pos,old_d),(pos,d),1000))
                    nodes.add((pos+d*(i-1),d))
                    edges.append(((pos,d),(pos+d*(i-1),d),(i-1)))
                    queue.append((pos+d*(i-1),d))
                    for d2 in [1,-1,1j,-1j]:
                            if d2 != d:
                                if (pos+d*(i-1), d2) in visited:
                                    edges.append(((pos+d*(i-1),d),(pos+d*(i-1),d2),1000))
    #create graph
    prance(maze,start,1)  
    #Dijkstra algorithm  
    previous = {n: None for n in nodes}
    distance = {n: inf for n in nodes}
    distance[(start,1)] = 0
    queue = nodes
    while len(queue) > 0:
        min_dist = inf
        min_cand = None
        for k in queue:
            if distance[k] < min_dist:
                min_dist = distance[k]
                min_cand = k
        if min_cand is not None:
            queue.remove(min_cand)
            for u in filter(lambda x: x[0] == min_cand, edges):
                alt = distance[min_cand] + u[2]
                if alt < distance[u[1]]:
                    distance[u[1]] = alt
                    previous[u[1]] = [min_cand]
                elif alt == distance[u[1]]:
                    previous[u[1]].append(min_cand)
    #end_distances = [distance[(end,d)] if (end,d) in distance else inf for d in [1,-1,1j,-1j]]
    #print(min(end_distances))

    end_distances = [distance[(end,d)] if (end,d) in distance else inf for d in [1,-1,1j,-1j]]
    shortest_distance = min(end_distances)

    visited = set([end])
    best_paths_queue = []
    for  d in [1,-1,1j,-1j]:
        if distance[(end,d)] == shortest_distance:
            for v in previous[(end,d)]:
                if v is not None:
                    p2,d2 = v
                    best_paths_queue.append(((end,d),(p2,d2)))
    while len(best_paths_queue) > 0:
        cand_bpq = best_paths_queue.pop(0)
        #print(cand_bpq)
        if cand_bpq[1] is not None:
            diff_x = int(cand_bpq[0][0].real - cand_bpq[1][0].real)
            diff_y = int(cand_bpq[0][0].imag - cand_bpq[1][0].imag)
            for i in range(abs(diff_x)):
                visited.add((cand_bpq[1][0] + (diff_x / abs(diff_x)) * i))
            for i in range(abs(diff_y)):
                visited.add((cand_bpq[1][0] + (diff_y / abs(diff_y)) * i * 1j))
            if previous[cand_bpq[1]] is not None:
                best_paths_queue.extend([(cand_bpq[1], v) for v in previous[cand_bpq[1]] if v is not None])
    print(len(visited))

    #for y in range(h):
    #    #
    #    print(''.join(['#' if maze[x+y*1j] == 1 else 'O' if x+y*1j in visited else '.' for x in range(w)]))

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