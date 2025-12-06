import operator
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2025/input/day05.txt','r') as input_file:
        rngs, ingrs = input_file.read().split('\n\n')
        ranges = []
        for rng in rngs.split('\n'):
            ranges.append(list(map(int,rng.split('-'))))
        ingredients = [int(ingr) for ingr in ingrs.split('\n')]
        return ranges, ingredients

def part_one():
    ranges, ingredients = parse_input()
    def fresh(n):
        for r in ranges:
            if r[0] <= n <= r[1]:
                return True
        return False
    fresh_count = sum([fresh(ing) for ing in ingredients])
    print(fresh_count)

def part_two():
    ranges, _ = parse_input()
    ranges.sort(key=operator.itemgetter(0))
    merged_ranges = [ranges[0]]
    for r in ranges[1:]:
        if r[0] <= merged_ranges[-1][1]:
            merged_ranges[-1][1] = max(merged_ranges[-1][1], r[1])
        else:
            merged_ranges.append(r)
    print(sum([r[1]-r[0]+1 for r in merged_ranges]))


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