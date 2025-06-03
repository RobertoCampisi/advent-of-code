import sys
import os
from collections import defaultdict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day14.txt','r') as input_file:
        reindeers = []
        for line in input_file.read().split('\n'):
            w = line.split(' ')
            reindeers.append((w[0],int(w[3]), int(w[6]), int(w[-2])))
        return reindeers

def part_one():
    time = 2503
    reindeers = parse_input()
    distances = []
    for r in reindeers:
        _, velocity, duration, rest = r
        d = (time // (duration + rest)) * velocity * duration
        d += min(velocity * duration, (time % (duration + rest) * velocity))
        distances.append(d)
    print(max(distances))

def part_two():
    reindeers = parse_input()
    score = defaultdict(lambda:0)
    distances = defaultdict(lambda:0)
    for i in range(2503):
        for r in reindeers:
            name, velocity, duration, rest = r
            if  i % (duration + rest) < duration:
                distances[name] += velocity
        score[max(distances, key= lambda key: distances[key])] += 1
    print(max(score.values()))





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