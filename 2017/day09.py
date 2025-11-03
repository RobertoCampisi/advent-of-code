import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2017/input/day09.txt','r') as input_file:
        return input_file.read()

def score(stream):
    depth = 1
    total = 0
    for c in stream:
        if c == '{':
            total += depth
            depth += 1
        else:
            depth -= 1
    return total

def part_one():
    stream = parse_input()
    #process ignores ( ! )
    stream = re.sub(r'\!.', '', stream)
    #remove garbage
    stream = re.sub(r'<.*?>', '', stream)
    #clean commas (assuming '{{,},{}}' == {{}{}})
    stream = re.sub(r',', '', stream)
    print(score(stream))

    

def part_two():
    stream = parse_input()
    #process ignores ( ! )
    stream = re.sub(r'\!.', '', stream)
    #turn all garbage into empty garbage
    stream_after_removal = re.sub(r'<.*?>', '<>', stream)
    print(stream_after_removal)
    print(len(stream)-len(stream_after_removal))

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