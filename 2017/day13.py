import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2017/input/day13.txt','r') as input_file:
        agents = {}
        for line in input_file.read().split('\n'):
            ws = line.split(':')
            agents[int(ws[0])] = int(ws[1])
        return agents

def part_one():
    firewall = parse_input()
    severity = 0
    for layer in firewall:
        if layer % (firewall[layer]*2-2) == 0:
            severity += layer * firewall[layer]
    print(severity)

def part_two():
    firewall = parse_input()
    #bruteforce solution
    for delay in range(100000000):
        caught = False
        for layer in firewall:
                if (layer+delay) % (firewall[layer]*2-2) == 0:
                    caught = True
        if not caught:
            print(delay)
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