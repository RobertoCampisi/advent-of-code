#import util functions
import sys

def parse_input():
    with open('2024/input/day1.txt','r') as input:
        return input.read().splitlines()

data = parse_input()

def part_one(data=data):
    left, right = [], []
    for line in data:
        l, r = list(map(int, line.split("   ")))
        left.append(l)
        right.append(r)
    print(sum([abs(a - b) for (a,b) in zip(sorted(left),sorted(right))]))


def part_two(data=data):
    left, right = [], {}
    for line in data:
        l, r = list(map(int, line.split("   ")))
        left.append(l)
        right[r] = right.get(r,0) + 1
    print(sum([a * right.get(a,0) for a in left]))

if __name__ == '__main__':
    globals()[sys.argv[1]]()