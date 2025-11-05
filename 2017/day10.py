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
    lengths = [ord(c) for c in "1,2,3"]
    print(lengths)
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
    #compute dense, something is going wrong here, Since empty string does not give the right result
    dense = circular_list[:16]
    for i in range(1,16): 
        for j in range(16):
            dense[j] ^= circular_list[i*16+j]
    print(dense)
    def hexify(n):
        hex_digits = [str(x) for x in range(10)] + ['a','b','c','d','e','f']
        d1 = n // 16
        d2 = n % 16
        return hex_digits[d1] + hex_digits[d2]

    hex_string = ''.join([hexify(x) for x in dense])
    print(hex_string)


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