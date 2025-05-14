import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2024/input/day24.txt','r') as input_file:
        return input_file.read().split("\n\n")

def part_one():
    initial_wires, gates = parse_input()
    wires = dict()
    for wire in initial_wires.split('\n'):
        tag, value = wire.split(': ')
        wires[tag] = value
    gate_queue = []
    for gate in gates.split('\n'):
        t1, g, t2, _, t3 = gate.split(' ')
        gate_queue.append([t1, t2, t3, g])
    i = 0
    while len(gate_queue) > 0:
        i = i % len(gate_queue)
        t1, t2, t3, g = gate_queue[i]
        if t1 in wires and t2 in wires:
            if g == 'AND':
                wires[t3] = '1' if wires[t1] == '1' and wires[t2] == '1' else '0'
            elif g == 'OR':
                wires[t3] = '1' if wires[t1] == '1' or wires[t2] == '1' else '0'
            elif g == 'XOR':
                wires[t3] = '1' if wires[t1] != wires[t2] else '0'
            gate_queue.pop(i)
        else:
            i += 1
    print(int(''.join([wires[tag] for tag in reversed(sorted(filter(lambda x: x.startswith('z'), wires)))]), 2))

def part_two():
    ...

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