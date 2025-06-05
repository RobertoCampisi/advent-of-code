import sys
import os
import math
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

# mana_cost, damage, heal, duration, armor, mana_recharge
spells = [(53, 4, 0, 1, 0, 0), (73, 2, 2, 1, 0, 0), (113, 0, 0, 6, 7, 0), (173, 3, 0, 6, 0, 0), (229, 0, 0, 5, 0, 101)]

def parse_input():
    with open('2015/input/day22.txt','r') as input_file:
        hp, damage = 0, 0
        for line in input_file.read().split('\n'):
            words = line.split(' ')
            if 'Hit Points' in line:
                hp = int(words[-1])
            elif 'Damage' in line:
                damage = int(words[-1])
        return [hp, damage]

def part_one():
    boss = parse_input()
    hp = 50
    mana = 500
    least_mana_spend = math.inf
    queue = [([0] * len(spells), [hp, mana, 0], boss, True)]
    while queue:
        active_spells, player, boss, player_turn = queue.pop(-1)
        armor = 0
        for i, spell_duration in enumerate(active_spells):
            if spell_duration > 0:
                player[0] += spells[i][2]
                armor += spells[i][4]
                boss[0] -= spells[i][1]
                player[1] += spells[i][5]
                active_spells[i] -= 1
        if boss[0] <= 0:
            least_mana_spend = min(least_mana_spend, player[2])
        elif player_turn:
            could_act = False
            for i, spell in enumerate(spells):
                if active_spells[i] == 0 and player[1] >= spells[i][0]:
                    could_act = True
                    new_player = [player[0], player[1] - spells[i][0], player[2] + spells[i][0]]
                    new_active_spells = active_spells.copy()
                    new_active_spells[i] += spells[i][3]
                    if new_player[2] < least_mana_spend:
                        queue.append((new_active_spells, new_player , boss.copy(), False))
            if not could_act and player[2] < least_mana_spend:
                queue.append((active_spells.copy(), player.copy(), boss.copy(), False))
        else:
            player[0] -= max(0,boss[1] - armor)
            if player[0] > 0 and player[2] < least_mana_spend:
                queue.append((active_spells.copy(), player.copy(), boss.copy(), True))
    print(least_mana_spend)

def part_two():
    boss = parse_input()
    hp = 50
    mana = 500
    least_mana_spend = math.inf
    queue = [([0] * len(spells), [hp, mana, 0], boss, True)]
    while queue:
        active_spells, player, boss, player_turn = queue.pop(-1)
        if player[0] > 0:
            if player_turn:
                player[0] -= 1
            armor = 0
            for i, spell_duration in enumerate(active_spells):
                if spell_duration > 0:
                    player[0] += spells[i][2]
                    armor += spells[i][4]
                    boss[0] -= spells[i][1]
                    player[1] += spells[i][5]
                    active_spells[i] -= 1
            if boss[0] <= 0:
                least_mana_spend = min(least_mana_spend, player[2])
            elif player_turn:
                could_act = False
                for i, spell in enumerate(spells):
                    if active_spells[i] == 0 and player[1] >= spells[i][0]:
                        could_act = True
                        new_player = [player[0], player[1] - spells[i][0], player[2] + spells[i][0]]
                        new_active_spells = active_spells.copy()
                        new_active_spells[i] += spells[i][3]
                        if new_player[2] < least_mana_spend:
                            queue.append((new_active_spells, new_player , boss.copy(), False))
                if not could_act and player[2] < least_mana_spend:
                    queue.append((active_spells.copy(), player.copy(), boss.copy(), False))
            else:
                player[0] -= max(0,boss[1] - armor)
                if player[0] > 0 and player[2] < least_mana_spend:
                    queue.append((active_spells.copy(), player.copy(), boss.copy(), True))
    print(least_mana_spend)

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