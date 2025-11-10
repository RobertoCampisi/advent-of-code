import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2017/input/day10.txt','r') as input_file:
        return input_file.read().split()[0]

def part_one():
    lengths = [int(x) for x in parse_input().split(',')]
    circular_list = list(range(256))
    selector = 0
    skip_size = 0
    for i,length in enumerate(lengths):
        def ci(index): #ciruclar index
            return index % len(circular_list)
        start_swap = selector
        end_swap = selector + length - 1
        while start_swap < end_swap:
            circular_list[ci(start_swap)],circular_list[ci(end_swap)] = circular_list[ci(end_swap)],circular_list[ci(start_swap)]
            start_swap+=1
            end_swap-=1
        selector = (selector + length + skip_size) % len(circular_list)
        skip_size += 1
    print(circular_list[0] * circular_list[1])

def part_two():
    lengths = [ord(c) for c in parse_input()] + [17, 31, 73, 47, 23]
    circular_list = list(range(256))
    selector = 0
    skip_size = 0
    #compute sparse list
    for _ in range(64):
      for i,length in enumerate(lengths):
          def ci(index): #ciruclar index
              return index % len(circular_list)
          start_swap = selector
          end_swap = selector + length - 1
          while start_swap < end_swap:
              circular_list[ci(start_swap)],circular_list[ci(end_swap)] = circular_list[ci(end_swap)],circular_list[ci(start_swap)]
              start_swap+=1
              end_swap-=1
          selector = (selector + length + skip_size) % len(circular_list)
          skip_size += 1
    dense = []
    for i in range(0,16):
        d =  circular_list[i*16]
        for j in range(1,16):
            d ^= circular_list[i*16+j]
        dense.append(d)
    print(''.join([f'{d:02x}' for d in dense]))


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