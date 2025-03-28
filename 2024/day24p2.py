from functools import lru_cache

initial_wires, gates = open("input.txt").read().split("\n\n")
wires = dict()
for wire in initial_wires.split('\n'):
    tag, value = wire.split(': ')
    wires[tag] = value

a = int(''.join([wires[tag] for tag in reversed(sorted(filter(lambda x: x.startswith('x'),wires)))]),2)
b = int(''.join([wires[tag] for tag in reversed(sorted(filter(lambda x: x.startswith('y'),wires)))]),2)

wires_backup = wires.copy()

structure_pointers = dict()
structure = [dict() for _ in range(46)]
gate_queue = []
for gate in gates.split('\n'):
    t1, g, t2, _, t3 = gate.split(' ')
    gate_queue.append([t1,t2,t3, g])

i = 0
halt_counter = 0
prev_len_gate_queue = len(gate_queue)
while len(gate_queue) > 0:
    if halt_counter == 2000:
        break
    if(prev_len_gate_queue) == len(gate_queue):
        halt_counter += 1
    else:
        halt_counter == 0
    prev_len_gate_queue = len(gate_queue)
    #print(structure_pointers)
    print(len(gate_queue))
    i = i % len(gate_queue)
    t1, t2, t3, g = gate_queue[i]
    if t1 in wires and t2 in wires:
        if g == 'AND' and t1[1:] == t2[1:]: # carry_p1
            structure[int(t1[1:])]['input1'] = t1
            structure[int(t1[1:])]['input2'] = t2
            if int(t1[1:]) > 0: 
                structure[int(t1[1:])]['carry_p1'] = t3
                structure_pointers[t3] = int(t1[1:])
            else:
                structure[int(t1[1:])+1]['carry_in'] = t3
                structure_pointers[t3] = int(t1[1:])+1
            wires[t3] = '1' if wires[t1] == '1' and  wires[t2] == '1' else '0'
        elif g == 'XOR' and t1[1:] == t2[1:]: #add_p1
            if int(t1[1:]) > 0:
                structure[int(t1[1:])]['add_p1'] = t3
            else:
                structure[int(t1[1:])]['out'] = t3
            structure_pointers[t3] = int(t1[1:])
            wires[t3] = '1' if wires[t1] != wires[t2]  else '0'
        elif g == 'XOR' and structure_pointers[t1] > 0 and 'carry_in' in structure[structure_pointers[t1]] and ((t1 == structure[structure_pointers[t1]]['add_p1'] and t2 == structure[structure_pointers[t1]]['carry_in']) or (t2 == structure[structure_pointers[t1]]['add_p1'] and t1 == structure[structure_pointers[t1]]['carry_in'])): #out
            structure[structure_pointers[t1]]['out'] = t3
            structure_pointers[t3] = structure_pointers[t1]
            wires[t3] = '1' if wires[t1] != wires[t2]  else '0'
        elif g == 'AND' and structure_pointers[t1] > 0 and 'carry_in' in structure[structure_pointers[t1]] and ((t1 == structure[structure_pointers[t1]]['add_p1'] and t2 == structure[structure_pointers[t1]]['carry_in']) or (t2 == structure[structure_pointers[t1]]['add_p1'] and t1 == structure[structure_pointers[t1]]['carry_in'])):
            structure[structure_pointers[t1]]['carry_p2'] = t3
            structure_pointers[t3] = structure_pointers[t1]
            wires[t3] = '1' if wires[t1] == '1' and  wires[t2] == '1' else '0'
        elif g == 'OR' and structure_pointers[t1] > 0 and 'carry_p2' in structure[structure_pointers[t1]] and ((t1 == structure[structure_pointers[t1]]['carry_p1'] and t2 == structure[structure_pointers[t1]]['carry_p2']) or (t2 == structure[structure_pointers[t1]]['carry_p1'] and t1 == structure[structure_pointers[t1]]['carry_p2'])):
            structure[structure_pointers[t1]+1]['carry_in'] = t3
            structure_pointers[t3] = structure_pointers[t1]+1
            wires[t3] = '1' if wires[t1] == '1' or  wires[t2] == '1' else '0'
        gate_queue.pop(i)
    else:
        i += 1
print(structure)
#print(wires)
#c = int(''.join([wires[tag] for tag in reversed(sorted(filter(lambda x: x.startswith('z'),wires)))]),2)

#simulate a full-adder
#def sim_full_adder(bit):
#    tag_x = ('x' + str(bit)) if bit > 9 else ('x0' + str(bit))
#    tag_y = ('y' + str(bit)) if bit > 9 else ('y0' + str(bit))
#    c_in, _ = sim_full_adder(bit-1) if bit > 0 else ('0', '0')
#    added_p1 = '1' if wires[tag_x] != wires[tag_y]  else '0'
#    added = '1' if added_p1  != c_in  else '0'
#    carry_p1 = '1' if wires[tag_x] == '1' and  wires[tag_y] == '1' else '0'
#    carry_p2 = '1' if added_p1 == '1' and  c_in == '1' else '0'
#    carry = '1' if carry_p1 == '1' or carry_p2 == '1' else '0'
#    return carry, added
#run simulation
#res = []
#for i in range(45):
#    tag_z = ('z' + str(i)) if i > 9 else ('z0' + str(i))
#    c, s = sim_full_adder(i)
#    print(tag_z,':',wires[tag_z],',sim:',s)
#    res.append(s)
#    if i == 44:
#        res.append(c)
#print(int(''.join(reversed(res)),2), a + b)
