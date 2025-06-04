import sys
import os
from itertools import combinations
import math
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

weapons = [(8,4,0),(10,5,0),(25,6,0),(40,7,0),(74,8,0)]
armor = [(13,0,1),(31,0,2),(53,0,3),(75,0,4),(102,0,5),(0,0,0)]
rings = [(25,1,0),(50,2,0),(100,3,0),(0,0,0),(20,0,1),(40,0,2),(80,0,3),(0,0,0)]

def parse_input():
    with open('2015/input/day21.txt','r') as input_file:
        hp, damage, defence = [0]*3
        for line in input_file.read().split('\n'):
            words = line.split(' ')
            if 'Hit Points' in line:
                hp = int(words[-1])
            elif 'Damage' in line:
                damage = int(words[-1])
            elif 'Armor' in line:
                defence = int(words[-1])
        return (hp, damage, defence)

def part_one():
    boss = parse_input()
    lowest_cost = math.inf
    for w in weapons:
        for a in armor:
            for r1,r2 in combinations(rings,2):
                cost, damage, defence = [sum(x) for x in zip(*[w,a,r1,r2])]
                boss_turns = math.inf
                if boss[1]-defence > 0:
                    boss_turns = int(math.ceil(100 / (boss[1]-defence)))
                player_turns = int(math.ceil(boss[0] / (damage-boss[2])))
                if player_turns <= boss_turns:
                    lowest_cost = min(lowest_cost, cost)
    print(lowest_cost)


def part_two():
    boss = parse_input()
    highest_cost = 0
    for w in weapons:
        for a in armor:
            for r1, r2 in combinations(rings, 2):
                cost, damage, defence = [sum(x) for x in zip(*[w, a, r1, r2])]
                boss_turns = math.inf
                if boss[1] - defence > 0:
                    boss_turns = int(math.ceil(100 / (boss[1] - defence)))
                player_turns = int(math.ceil(boss[0] / (damage - boss[2])))
                if player_turns > boss_turns:
                    highest_cost = max(highest_cost, cost)
    print(highest_cost)

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