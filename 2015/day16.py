import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day16.txt','r') as input_file:
        sues = {}
        for line in input_file.read().split('\n'):
            _, idx, c1, n1, c2, n2, c3, n3 = line.replace(':','').replace(',','').split(' ')
            sues[idx] = {c1 : int(n1), c2 : int(n2), c3: int(n3)}
        return sues

gift_sue = {'children': 3, 'cats': 7, 'samoyeds': 2,
        'pomeranians': 3, 'akitas': 0, 'vizslas': 0,
        'goldfish': 5, 'trees': 3, 'cars': 2 ,'perfumes': 1}

def is_MFCSAM_subset(a,b=gift_sue):
    for k,v in a.items():
        if k == 'cats' or k == 'trees':
            if v <= gift_sue[k]:
                return False
        elif k == 'pomeranians' or k == 'goldfish':
            if v >= gift_sue[k]:
                return False
        elif v != gift_sue[k]:
            return False
    return True

def part_one():
    sues = parse_input()
    for i, sue in sues.items():
        if sue.items() <= gift_sue.items():
            print(i)
            break


def part_two():
    sues = parse_input()
    for i, sue in sues.items():
        if is_MFCSAM_subset(sue):
            print(i)
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