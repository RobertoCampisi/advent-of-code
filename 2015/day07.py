import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day07.txt','r') as input_file:
        gate_queue = []
        for instruction in input_file.read().split('\n'):
            if re.search(r'NOT', instruction):
                _, t1, _ , t2 = instruction.split(' ')
                gate_queue.append(('NOT',0, [t1], t2))
            elif re.search(r'SHIFT', instruction):
                t1, g, lit , _ , t2 = instruction.split(' ')
                gate_queue.append((g, int(lit), [t1], t2))
            elif re.search(r'AND|OR', instruction):
                t1, g, t2 , _ , t3 = instruction.split(' ')
                if re.match(r'\d+', t1):
                    gate_queue.append((g+'_LIT', int(t1), [t2], t3))
                else:
                    gate_queue.append((g, 0, [t1, t2], t3))
            else:
                cand, _, t1 = instruction.split(' ')
                if re.match(r'\d+', cand):
                    gate_queue.append(('ASSIGN_LIT', int(cand), [], t1))
                else:
                    gate_queue.append(('ASSIGN', 0, [cand], t1))
        return gate_queue

def emulate(gate_queue):
    wires = dict()
    i = 0
    while len(gate_queue) > 0:
        i = i % len(gate_queue)
        opcode, literal, input_, output = gate_queue[i]
        if all(i in wires for i in input_) or len(input_) == 0:
            match opcode:
                case 'ASSIGN_LIT': wires[output] = literal
                case 'ASSIGN': wires[output] = wires[input_[0]]
                case 'NOT': wires[output] = ~wires[input_[0]]
                case 'LSHIFT': wires[output] = wires[input_[0]] << literal
                case 'RSHIFT': wires[output] = wires[input_[0]] >> literal
                case 'AND': wires[output] = wires[input_[0]] & wires[input_[1]]
                case 'OR': wires[output] = wires[input_[0]] | wires[input_[1]]
                case 'AND_LIT': wires[output] = literal & wires[input_[0]]
                case 'OR_LIT': wires[output] = literal | wires[input_[0]]
            gate_queue.pop(i)
        else:
            i += 1
    return wires

def part_one():
    gate_queue = parse_input()
    wires = emulate(gate_queue)
    print(wires['a'])

def part_two():
    gate_queue = parse_input()
    wires = emulate(gate_queue)
    new_b = wires['a']
    gate_queue = parse_input()
    #overwrite wire b
    for i in range(len(gate_queue)):
        opcode, literal, _, output = gate_queue[i]
        if opcode == 'ASSIGN_LIT' and output == 'b':
            gate_queue[i] = ('ASSIGN_LIT',new_b,[],output)
    wires = emulate(gate_queue)
    print(wires['a'])


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