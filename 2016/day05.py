import sys
import os
from hashlib import md5
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2016/input/day05.txt','r') as input_file:
        return input_file.read().strip()

def part_one():
    door_id = parse_input()
    index = 0
    hash = md5((door_id + str(index)).encode())
    password = ''
    while len(password) <= 7:
        while not hash.hexdigest().startswith('00000'):
            index += 1
            hash =  md5((door_id + str(index)).encode())
        password += hash.hexdigest()[5]
        index += 1
        hash = md5((door_id + str(index)).encode())
    print(password)

def part_two():
    door_id = parse_input()
    index = 0
    hash = md5((door_id + str(index)).encode())
    password = '_'*8
    while '_' in password:
        while not hash.hexdigest().startswith('00000'):
            index += 1
            hash =  md5((door_id + str(index)).encode())
        character_index = int(hash.hexdigest()[5], 16)
        if 0 <= character_index <= 7 and password[character_index] == '_':
          password = password[:character_index] + hash.hexdigest()[6] + password[character_index+1:]
          #print(password) #uncomment for password shaping animation
        index += 1
        hash = md5((door_id + str(index)).encode())
    print(password)

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