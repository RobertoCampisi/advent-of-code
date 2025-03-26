from functools import lru_cache

initial_wires, gates = open("input.txt").read().split("\n\n")
wires = dict()
for wire in initial_wires.split('\n'):
    tag, value = wire.split(': ')
    wires[tag] = value

gate_queue = []
for gate in gates.split('\n'):
    t1, g, t2, _, t3 = gate.split(' ')
    gate_queue.append([t1,t2,t3, g])

i = 0
while len(gate_queue) > 0:
    i = i % len(gate_queue)
    t1, t2, t3, g = gate_queue[i]
    if t1 in wires and t2 in wires:
        if g == 'AND':
            wires[t3] = '1' if wires[t1] == '1' and  wires[t2] == '1' else '0'
        elif g == 'OR':
            wires[t3] = '1' if wires[t1] == '1' or  wires[t2] == '1' else '0'
        elif g == 'XOR':
            wires[t3] = '1' if wires[t1] != wires[t2]  else '0'
        gate_queue.pop(i)
    else:
        i += 1

print(int(''.join([wires[tag] for tag in reversed(sorted(filter(lambda x: x.startswith('z'),wires)))]),2))
