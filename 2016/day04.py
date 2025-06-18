import sys
import os
import re
from collections import defaultdict
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2016/input/day04.txt','r') as input_file:
        rooms = [] #room: [name, sector id, checksum]
        for line in input_file.read().split('\n'):
            words = line.split('-')
            name = '-'.join(words[:-1])
            sector_id, checksum = re.search(r'(\d+)\[([a-z]{5})\]',words[-1]).group(1, 2) 
            rooms.append([name, int(sector_id), checksum])
        return rooms

def valid_checksum(name, checksum):
    letter_freq = defaultdict(lambda: 0)
    for letter in name:
        if letter != '-':
            letter_freq[letter] += 1
    letter_freq = sorted(letter_freq.items(), key=lambda x: (-x[1], x[0]))
    return ''.join([x[0] for x in letter_freq[:5]]) == checksum

def decrypt_swift_cipher(string_, steps):
    n_letters = ord('z') - ord('a') + 1
    return ''.join([
                ' ' if letter == '-' 
                else chr(ord('a') + ((ord(letter) - ord('a'))+ steps) % n_letters) 
                for letter in string_
            ]) 

def part_one():
    rooms = parse_input()
    real_rooms_sum = 0
    for name,sector_id,checksum in rooms:
        if valid_checksum(name, checksum):
            real_rooms_sum += sector_id
    print(real_rooms_sum)

def part_two():
    real_rooms = filter(lambda x: valid_checksum(x[0],x[2]),parse_input())
    for name,sector_id,_ in real_rooms:
        if re.search(r'north',decrypt_swift_cipher(name, sector_id)):
            print(sector_id)
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