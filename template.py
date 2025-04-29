import sys
#import util functions

def parse_input():
    with open('{0}/input/day{1}.txt','r') as input_file:
        return ...

data = parse_input()

def part_one():
    ...

def part_two():
    ...

def benchmark(func, n):
    from time import time
    start = time()
    for i in range(0, n):
        func()
    end = time()
    print((end - start) / n)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        globals()[sys.argv[1]]()
    elif len(sys.argv) > 2:
        globals()[sys.argv[1]](*sys.argv[2:])
    else:
        raise RuntimeError