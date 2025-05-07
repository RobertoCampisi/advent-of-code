import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2024/input/day9.txt','r') as input_file:
        line = input_file.read().strip().split("\n")[0]
        data = dict()
        id_counter = 0
        k = 0
        for i, digit in enumerate(line):
            d = int(digit)
            if i % 2 == 0:
                data[k] = (id_counter, d)
                id_counter += 1
            else:
                data[k] = (None, d)
            k += d
        return data, k

def part_one():
    data2, _ = parse_input()
    #flatten dict
    data = [data2[k][0] for k in data2.keys() for _ in range(data2[k][1])]
    k = 0
    l = len(data) - 1
    checksum = 0
    while k <= l:
        if data[k] is None:
            if data[l] is not None:
                data[k], data[l] = data[l], data[k]
                checksum += data[k] * k
                l -= 1
                k += 1
            else:
                l -= 1
        else:
            checksum += data[k] * k
            k += 1
    print(checksum)

def part_two():
    data, k = parse_input()
    key = 0
    while key < k:
        # fillable slot
        if data[key][0] is None:
            for rkey in reversed(sorted(data.keys())):
                if data[rkey][0] is not None:
                    if rkey < key:
                        key += data[key][1]
                        break
                    if data[rkey][1] <= data[key][1]:
                        diff = data[key][1] - data[rkey][1]
                        data[key] = (data[rkey][0], data[rkey][1])
                        data[rkey] = (None, data[rkey][1])
                        if diff > 0:
                            data[key + data[rkey][1]] = (None, diff)
                        key += data[key][1]
                        break
        else:
            key += data[key][1]
    checksum = 0
    for key in sorted(data.keys()):
        id, l = data[key]
        if id is not None:
            for i in range(l):
                checksum += id * (key + i)
    print(checksum)

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