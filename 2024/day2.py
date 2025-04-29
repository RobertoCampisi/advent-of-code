import sys
#import util functions

def parse_input():
    with open('2024/input/day2.txt','r') as input_file:
        return [list(map(int,line.strip().split(' '))) for line in input_file.readlines()]

data = parse_input()

def is_safe_with_dampener(report):
    if is_safe(report):
        return True
    else:
        for i in range(len(report)):
            if is_safe(report[:i] + report[i+1:]):
                return True
    return False

def is_safe(report):
    diffs = [b-a for (a,b) in zip(report[:-1], report[1:])]
    first = diffs[0]
    for d in diffs[1:]:
        if 0 > first >= -3: #all negative
            if d >= 0 or d < -3:
                return False
        elif 0 < first <= 3: #all positive
            if d <= 0 or d > 3:
                return False
        else:
            return False
    return True

def part_one():
    print([is_safe(line) for line in data].count(True))


def part_two():
    print([is_safe_with_dampener(line) for line in data].count(True))

if __name__ == '__main__':
    globals()[sys.argv[1]]()