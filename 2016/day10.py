import sys
import os
from collections import defaultdict
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2016/input/day10.txt','r') as input_file:
        bots = defaultdict(lambda:[])
        botcommands = defaultdict(lambda:(None,None))
        botqueue = []
        for ins in input_file.read().split('\n'):
            words = ins.split()
            if len(words) == 6: #input
                bot = int(words[5])
                bots[bot] += [int(words[1])]
                if len(bots[bot]) > 1:
                    botqueue.append(bot)
            else: #botcommand
                bot = int(words[1])
                t1 = words[5:7]
                t2 = words[10:12]
                botcommands[bot] = (t1,t2)
        return bots, botcommands, botqueue

def part_one():
    bots, b_commands, b_queue = parse_input()
    output = defaultdict(lambda:0)
    while b_queue:
        bot = b_queue.pop(0)
        ins = b_commands[bot]
        v = bots[b_queue]
        if v[0] < v[1]:
            

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