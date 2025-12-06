import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions
from operator import itemgetter
def parse_input():
    with open('2025/input/day03.txt','r') as input_file:
        return [[int(x) for x in list(line)] for line in input_file.read().split('\n')]

# Returns a tuple with the index of the highest and second highest of the given array
def highest_two_index(arr):
    h_idx = 0
    prev_h_idx = 0
    for i,e in enumerate(arr):
        if e >= arr[h_idx] and e> arr[prev_h_idx]:
            prev_h_idx, h_idx = h_idx, i
    return h_idx, prev_h_idx

def part_one():
    banks = parse_input()
    joltage_total = 0
    for battery_bank in banks:
        h1, h2 = highest_two_index(battery_bank)
        h1n, _ = highest_two_index(battery_bank[h1+1:])
        h2n, _ = highest_two_index(battery_bank[h2+1:])
        cand2 = battery_bank[h2]*10+battery_bank[h2+h2n+1]
        if h1+1 == len(battery_bank):
            joltage_total += cand2
        else:
            cand1 = battery_bank[h1]*10+battery_bank[h1+h1n+1]
            if cand1 > cand2:
                joltage_total += cand1
            else:
                joltage_total += cand2
    print(joltage_total)


def largest_number(digits, arr):
    if digits == 0:
        return []
    largest_index = max(enumerate(arr[:-(digits-1)] if digits > 1 else arr),key=itemgetter(1))[0]
    return [arr[largest_index]] + largest_number(digits-1, arr[largest_index+1:])

def part_two():
    banks = parse_input()
    joltage_total = 0
    for battery_bank in banks:
        joltage = int(''.join([str(x) for x in largest_number(12,battery_bank)]))
        joltage_total += joltage
    print(joltage_total)

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