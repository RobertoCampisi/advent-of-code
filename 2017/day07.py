import sys
import os
from collections import defaultdict
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2017/input/day07.txt','r') as input_file:
        input_data = []
        for line in input_file.read().split("\n"):
            words = line.split()
            weight = int(words[1][1:-1])
            children = [w.replace(',','') for w in words[3:]]
            input_data.append({'name':words[0], 'weight':weight, 'children':children})
        return input_data

def part_one():
    input_relations = parse_input()
    parent_of = defaultdict(lambda: None)
    seen_nodes = set()
    for rel in input_relations:
        seen_nodes.add(rel['name'])
        for child in rel['children']:
            seen_nodes.add(child)
            parent_of[child] = rel['name']
    for node in seen_nodes:
        if parent_of[node] is None:
            print(node)

def part_two():
    input_relations = parse_input()
    children = defaultdict(lambda: None)
    parent_of = defaultdict(lambda: None)
    individual_weights = defaultdict(lambda: 0)
    total_weights = defaultdict(lambda: 0)
    seen_nodes = set()
    #fill dictionaries
    for rel in input_relations:
        seen_nodes.add(rel['name'])
        children[rel['name']] = rel['children']
        individual_weights[rel['name']] = rel['weight']
        for child in rel['children']:
            seen_nodes.add(child)
            parent_of[child] = rel['name']
    #find root
    root = None
    for node in seen_nodes:
        if parent_of[node] is None:
            root = node
    #compute disc weights
    if root is not None:
      def get_weight_subtree(node):
          total_weight_disc = individual_weights[node] + sum([get_weight_subtree(c) for c in children[node]])
          total_weights[node] = total_weight_disc
          return total_weight_disc
      get_weight_subtree(root)
      #find imbalance
      current = root
      target_weight = 0
      for i in range(100):
          ws = defaultdict(lambda: 0)
          for child in children[current]:
              ws[total_weights[child]] += 1
          next_target_weight = list(filter(lambda x: x[1] > 1, ws.items()))[0][0]
          imbalance_weight = list(filter(lambda x: x[1] == 1, ws.items())) 
          if imbalance_weight:
              for child in children[current]:
                  if total_weights[child] == imbalance_weight[0][0]:
                    current = child 
                    target_weight = next_target_weight
          else:
              print(target_weight - total_weights[current] + individual_weights[current])
              break

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