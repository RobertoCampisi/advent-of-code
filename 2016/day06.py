import sys
import os
from collections import defaultdict
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2016/input/day06.txt','r') as input_file:
        return input_file.read().split('\n')

def part_one():
    messages = parse_input()
    frequency_dicts = [defaultdict(lambda: 0) for _ in range(len(messages[0]))]
    for message in messages:
      for i,character in enumerate(message):
          frequency_dicts[i][character] += 1
    highest_frequency_characters = ''.join([max(d, key=d.get) for d in frequency_dicts])
    print(highest_frequency_characters) 

def part_two():
    messages = parse_input()
    frequency_dicts = [defaultdict(lambda: 0) for _ in range(len(messages[0]))]
    for message in messages:
      for i,character in enumerate(message):
          frequency_dicts[i][character] += 1
    highest_frequency_characters = ''.join([min(d, key=d.get) for d in frequency_dicts])
    print(highest_frequency_characters) 

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