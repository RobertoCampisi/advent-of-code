from functools import lru_cache
from dataclasses import dataclass
from typing import List

@dataclass
class Node:
    name: str
    edges: List['Node']

#construct graph
graph = dict()
for edge in open("input.txt"):
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
