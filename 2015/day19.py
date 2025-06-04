import sys
import os
from collections import defaultdict
import re
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day19.txt','r') as input_file:
        replacements_, molecule_ = input_file.read().split('\n\n') 
        molecule = re.findall(r'[A-Z][a-z]*',molecule_)
        replacements = defaultdict(lambda: [])
        for line in replacements_.split('\n'):
            i, _, o = line.split(' ')
            replacements[i] += [o]
        return replacements, molecule

def part_one():
    replacements, molecule = parse_input()
    molecules = set()
    for i,atom in enumerate(molecule):
        for r in replacements[atom]:
            new_molucule = ''.join(molecule[:i]+[r]+molecule[i+1:])
            molecules.add(new_molucule)
    print(len(molecules))

def part_two():
    replacements, molecule = parse_input()
    replacements_T = defaultdict(lambda:[])
    for k,v in replacements.items():
        for r in v:
            replacements_T[r] += [k]
    molecules = set([''.join(molecule)])
    steps = 0
    print(replacements_T)
    for _ in range(1000):
        next_molecules = set()
        for m in molecules:
            for k, v in replacements_T.items():
                pattern = re.compile(k)
                i = 0
                pm = pattern.search(m,i)
                while pm is not None:
                    for r in v:
                        next_molecules.add(m[:pm.start()] + r + m[pm.end():])
                    i =  pm.start() + 1 
                    pm = pattern.search(m,i)
        steps += 1
        if 'e' in next_molecules:
            break
        molecules = set(sorted(list(next_molecules),key=len)[:10])
    print(steps)

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