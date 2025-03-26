from functools import lru_cache

initial_wires, gates = open("input.txt").read().split("\n\n")
wires = dict()
for wire in initial_wires.split('\n'):
    tag, value = wire.split(': ')
    wires[tag] = value

a = int(''.join([wires[tag] for tag in reversed(sorted(filter(lambda x: x.startswith('x'),wires)))]),2)
b = int(''.join([wires[tag] for tag in reversed(sorted(filter(lambda x: x.startswith('y'),wires)))]),2)

wires_backup = wires.copy()

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
print(wires)

c = int(''.join([wires[tag] for tag in reversed(sorted(filter(lambda x: x.startswith('z'),wires)))]),2)

#simulate a full-adder
def sim_full_adder(bit):
    tag_x = ('x' + str(bit)) if bit > 9 else ('x0' + str(bit))
    tag_y = ('y' + str(bit)) if bit > 9 else ('y0' + str(bit))
    c_in, _ = sim_full_adder(bit-1) if bit > 0 else ('0', '0')
    added_p1 = '1' if wires[tag_x] != wires[tag_y]  else '0'
    added = '1' if added_p1  != c_in  else '0'
    carry_p1 = '1' if wires[tag_x] == '1' and  wires[tag_y] == '1' else '0'
    carry_p2 = '1' if added_p1 == '1' and  c_in == '1' else '0'
    carry = '1' if carry_p1 == '1' or carry_p2 == '1' else '0'
    return carry, added
#run simulation
res = []
for i in range(45):
    tag_z = ('z' + str(i)) if i > 9 else ('z0' + str(i))
    c, s = sim_full_adder(i)
    print(tag_z,':',wires[tag_z],',sim:',s)
    res.append(s)
    if i == 44:
        res.append(c)
print(int(''.join(reversed(res)),2), a + b)


