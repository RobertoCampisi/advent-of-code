import sys
import os
from dataclasses import dataclass
from typing import List
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

@dataclass
class Node:
    name: str
    edges: List['Node']

def parse_input():
    with open('2024/input/day23.txt','r') as input_file:
        graph = dict()
        for edge in input_file:
            n1, n2 = edge.strip().split('-')
            if n1 in graph and n2 in graph: 
                graph[n1].edges.append(graph[n2])
                graph[n2].edges.append(graph[n1])
            elif n1 in graph:
                t2 = Node(n2,[graph[n1]])
                graph[n2] = t2
                graph[n1].edges.append(graph[n2])
            elif n2 in graph:
                t1 = Node(n1,[graph[n2]])
                graph[n1] = t1
                graph[n2].edges.append(graph[n1])
            else:
                t1 = Node(n1,[])
                graph[n1] = t1
                t2 = Node(n2,[graph[n1]])
                graph[n2] = t2
                graph[n1].edges.append(graph[n2])
        return graph

def part_one():
    graph = parse_input()
    interlinked_t_set = [] #this list will be used to simulate a set of sets.
    #construct the interlinked set containing all sets which contains a node that starts with t
    for node in graph.values():
        for e1 in node.edges:
            for e2 in node.edges:
                if e1.name != e2.name and e1 in e2.edges and e2 in e1.edges:
                    candidate_set = set([node.name, e1.name, e2.name])
                    if node.name.startswith('t') or e1.name.startswith('t') or e2.name.startswith('t'):
                        if candidate_set not in interlinked_t_set:
                            interlinked_t_set.append(candidate_set)
    print(len(interlinked_t_set))

def part_two():
    graph = parse_input()
    cliques = []
    for node in graph.values():
        cliques.append([node.name])
    for node in graph.values():
        for i,c in enumerate(cliques):
            if all([x in [e.name for e in node.edges] for x in c]):
                cliques[i].append(node.name)
    max_clique = []
    for c in cliques:
        if len(c) > len(max_clique):
            max_clique = c
    print(','.join(sorted(max_clique)))

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