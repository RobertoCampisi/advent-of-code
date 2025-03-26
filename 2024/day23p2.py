from functools import lru_cache
from dataclasses import dataclass
from typing import List

@dataclass
class Node:
    name: str
    edges: List['Node']

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
