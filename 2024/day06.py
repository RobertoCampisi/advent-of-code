import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions
from my_utils import tadd

def parse_input():
    with open('2024/input/day06.txt','r') as input_file:
        lines = input_file.read().strip().split("\n")
        width = len(lines[0])
        height = len(lines)
        start_position = (0, 0)
        rows = dict()
        cols = dict()
        for i,line in enumerate(lines):
            if re.search(r'#', line) is not None:
                obstacles = re.finditer(r'#', line)
                for o in obstacles:
                    j = o.span()[0]
                    rows[i] = rows.get(i, []) + [j]
                    cols[j] = cols.get(j, []) + [i]
            if re.search(r'\^', line) is not None:
                start_position = (re.search(r'\^', line).span()[0],i)
        return width, height, lines, rows, cols, start_position

def part_one():
    width, height, lines, rows, cols, start_position = parse_input()
    #predict path length
    pos = start_position
    direction = 0 # 0 = up, 1 = right, 2=down, 3=left
    counter = 0
    visited = set()
    visited.add(start_position)
    while counter < 1<<20:
        x, y = pos
        encountered = False
        if direction == 0:
            if x in cols:
                #print(x, cols[x])
                for o in reversed(cols[x]):
                    if o < y:
                        pos = (x, o+1)
                        encountered = True
                        for i in range(o+1,y):
                            visited.add((x,i))
                        break
            if not encountered:
                for i in range(0, y):
                    visited.add((x, i))
                break
        elif direction == 1:
            if y in rows:
                #print(y,rows[y])
                for o in rows[y]:
                    if o > x:
                        pos = (o-1, y)
                        encountered = True
                        for i in range(x,o-1):
                            visited.add((i,y))
                        break
            if not encountered:
                for i in range(x, width):
                    visited.add((i, y))
                break
        elif direction == 2:
            if x in cols:
                #print(x,cols[x])
                for o in cols[x]:
                    if o > y:
                        pos = (x, o-1)
                        encountered = True
                        for i in range(y, o):
                            visited.add((x, i))
                        break
            if not encountered:
                for i in range(y, height):
                    visited.add((x, i))
                break
        else:
            if y in rows:
                #print(y, rows[y])
                for o in reversed(rows[y]):
                    if o < x:
                        pos = (o+1, y)
                        encountered = True
                        for i in range(o+1,x):
                            visited.add((i,y))
                        break
            if not encountered:
                for i in range(0, x):
                    visited.add((i, y))
                break
        direction = (direction + 1) % 4
        counter += 1

    for (x, y) in visited:
        lines[y] = lines[y][:x] + 'X' + lines[y][x + 1:]
    lines[pos[1]] = lines[pos[1]][:pos[0]] + '^' + lines[pos[1]][pos[0] + 1:]
    #for i, line in enumerate(lines):
    #    print(line)
    print(len(visited))

def part_two():
    width, height, lines, rows, cols, start_position = parse_input()
    # predict path length
    pos = start_position
    direction = 0 # 0 = up, 1 = right, 2=down, 3=left
    counter = 0
    visited = set()
    visited.add(start_position)
    while counter < 1000:
        x, y = pos
        encountered = False
        if direction == 0:
            if x in cols:
                # print(x, cols[x])
                for o in reversed(cols[x]):
                    if o < y:
                        pos = (x, o + 1)
                        encountered = True
                        for i in range(o + 1, y):
                            visited.add((x, i))
                        break
            if not encountered:
                for i in range(0, y):
                    visited.add((x, i))
                break
        elif direction == 1:
            if y in rows:
                # print(y,rows[y])
                for o in rows[y]:
                    if o > x:
                        pos = (o - 1, y)
                        encountered = True
                        for i in range(x, o - 1):
                            visited.add((i, y))
                        break
            if not encountered:
                for i in range(x, width):
                    visited.add((i, y))
                break
        elif direction == 2:
            if x in cols:
                # print(x,cols[x])
                for o in cols[x]:
                    if o > y:
                        pos = (x, o - 1)
                        encountered = True
                        for i in range(y, o):
                            visited.add((x, i))
                        break
            if not encountered:
                for i in range(y, height):
                    visited.add((x, i))
                break
        else:
            if y in rows:
                # print(y, rows[y])
                for o in reversed(rows[y]):
                    if o < x:
                        pos = (o + 1, y)
                        encountered = True
                        for i in range(o + 1, x):
                            visited.add((i, y))
                        break
            if not encountered:
                for i in range(0, x):
                    visited.add((i, y))
                break

        direction = (direction + 1) % 4
        counter += 1

    # check for potential loops by putting an obstacle on each visited position from the original path.
    total_counter = 0
    for v in visited:
        if v is not start_position:
            new_rows = rows.copy()
            new_cols = cols.copy()
            # put down obstacle
            new_rows[v[1]] = sorted(rows.get(v[1], []) + [v[0]])
            new_cols[v[0]] = sorted(cols.get(v[0], []) + [v[1]])
            # cycle detection
            new_visited = set()
            new_visited.add(start_position)
            pos = start_position
            counter = 0
            direction = 0
            cycle_counter = 0
            prev_len_new_visited = 0
            while counter < 100000:
                x, y = pos
                encountered = False
                if direction == 0:
                    if x in new_cols:
                        for o in reversed(new_cols[x]):
                            if o < y:
                                pos = (x, o + 1)
                                encountered = True
                                for i in range(o + 1, y):
                                    new_visited.add((x, i))
                                break
                    if not encountered:
                        for i in range(0, y):
                            new_visited.add((x, i))
                        break
                elif direction == 1:
                    if y in new_rows:
                        for o in new_rows[y]:
                            if o > x:
                                pos = (o - 1, y)
                                encountered = True
                                for i in range(x, o - 1):
                                    new_visited.add((i, y))
                                break
                    if not encountered:
                        for i in range(x, width):
                            new_visited.add((i, y))
                        break
                elif direction == 2:
                    if x in new_cols:
                        for o in new_cols[x]:
                            if o > y:
                                pos = (x, o - 1)
                                encountered = True
                                for i in range(y, o):
                                    new_visited.add((x, i))
                                break
                    if not encountered:
                        for i in range(y, height):
                            new_visited.add((x, i))
                        break
                else:
                    if y in new_rows:
                        for o in reversed(new_rows[y]):
                            if o < x:
                                pos = (o + 1, y)
                                encountered = True
                                for i in range(o + 1, x):
                                    new_visited.add((i, y))
                                break
                    if not encountered:
                        for i in range(0, x):
                            new_visited.add((i, y))
                        break

                direction = (direction + 1) % 4
                if cycle_counter > 3:
                    total_counter += 1
                    break
                if len(new_visited) == prev_len_new_visited:
                    cycle_counter += 1
                else:
                    prev_len_new_visited = len(new_visited)
                counter += 1
    print(total_counter)

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