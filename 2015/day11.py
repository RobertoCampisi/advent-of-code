import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2015/input/day11.txt','r') as input_file:
        return input_file.read().strip()

#find next candidate that does not include invalid characters
def next_candidate_password(password):
    skip_char = {'i':'j','o':'p','l':'m'}
    if any([sc in password for sc in skip_char.keys()]):
        first_skip_index = min(filter(lambda x: x >= 0, [password.find(sc) for sc in skip_char]))
        return password[:first_skip_index] + skip_char[password[first_skip_index]] + 'a' * (len(password) - first_skip_index - 1)
    next_password = ''
    for i,c in list(enumerate(password))[::-1]:
        if ord(c)+1 <= ord('z'):
            cand = chr(ord(c) + 1)
            if cand in skip_char.keys():
                cand = skip_char[cand]
            next_password = password[:i] + cand + next_password
            break
        else:
            next_password += 'a'
    return next_password

def is_valid(password):
    double_letters = [ i == j for i,j in zip(password[:-1], password[1:])]
    return (
        sum(double_letters) >= 2 #check for pairs of letters
        and not any([i & j for i,j in zip(double_letters[:-1], double_letters[1:])]) #check for overlapping double_letters
        #check for increasing triplet
        and any([ ord(i) + 1 == ord(j) and ord(i) + 2 == ord(k) for i,j,k in zip(password[:-2], password[1:-1], password[2:])])
    )

def part_one():
    password = parse_input()
    while not is_valid(password):
        password = next_candidate_password(password)
    print(password)

def part_two():
    password = parse_input()
    while not is_valid(password):
        password = next_candidate_password(password)
    password = next_candidate_password(password)
    while not is_valid(password):
        password = next_candidate_password(password)
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