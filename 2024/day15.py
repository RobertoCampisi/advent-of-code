import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input(map_changes):
    with open('2024/input/day15.txt','r') as input_file:
        input1, input2 = input_file.read().split("\n\n")
        #grid = [list(line) for line in input1.splitlines()]
        grid = [list(''.join(map(lambda x: map_changes[x],line))) for line in input1.splitlines()]
        commands = ''.join([i.strip() for i in input2.splitlines()])
        for i,row in enumerate(grid):
            for j,col in enumerate(row): 
                if grid[i][j] == "@":
                    bot_pos = (i,j)
                    break
        return grid, commands, bot_pos

def move_bot(pos, command):
    row, col = pos
    if push_boxes(pos, command):
        if command == "<":
            col -= 1
        elif command == ">":
            col += 1
        elif command == "^":
            row -= 1
        elif command == "v":
            row += 1
    return (row, col)

def push_boxes(pos,command):
    if attempt_push(pos,command):
        #print("shoving box!")
        move_boxes(pos,command)
        return True
    else:
        return False

def attempt_push(pos,command):
    global grid
    row, col = pos
    if command == "<":
        target = grid[row][col-1]
        if target == ".":
            return True
        elif target == "#":
            return False
        else:
            return attempt_push((row, col-1), command)
    elif command == ">":
        target = grid[row][col+1]
        if target == ".":
            return True
        elif target == "#":
            return False
        else:
            return attempt_push((row, col+1), command)
    elif command == "^":
        target = grid[row-1][col]
        if target == ".":
            return True
        elif target == "#":
            return False
        else:
            if target == "[":
                return attempt_push((row-1, col),command) and attempt_push((row-1, col+1), command)
            elif target == "]":
                return attempt_push((row-1, col-1),command) and attempt_push((row-1, col), command)
            else:
                return attempt_push((row-1, col), command)
    elif command == "v":
        target = grid[row+1][col]
        if target == ".":
            return True
        elif target == "#":
            return False
        else:
            if target == "[":
                return attempt_push((row+1, col),command) and attempt_push((row+1, col+1), command)
            elif target == "]":
                return attempt_push((row+1, col-1),command) and attempt_push((row+1, col), command)
            else:
                return attempt_push((row+1, col), command)
    else:
        return False

    
def move_boxes(pos,command):
    global grid
    row, col = pos
    if command == "<":
        target = grid[row][col-1]
        if target == ".":
            grid[row][col-1],grid[row][col] = grid[row][col],grid[row][col-1]
        elif target != "#":
            move_boxes((row, col-1), command)
            grid[row][col-1],grid[row][col] = grid[row][col],grid[row][col-1]
    elif command == ">":
        target = grid[row][col+1]
        if target == ".":
            grid[row][col+1],grid[row][col] = grid[row][col],grid[row][col+1]
        elif target != "#":
            move_boxes((row, col+1), command)
            grid[row][col+1],grid[row][col] = grid[row][col],grid[row][col+1]
    elif command == "^":
        target = grid[row-1][col]
        if target == ".":
            grid[row-1][col],grid[row][col] = grid[row][col],grid[row-1][col]
        elif target != "#":
            if target == "[":
                move_boxes((row-1, col+1), command)
            elif target == "]":
                move_boxes((row-1, col-1),command)
            move_boxes((row-1, col), command)
            grid[row-1][col],grid[row][col] = grid[row][col],grid[row-1][col]
    elif command == "v":
        target = grid[row+1][col]
        if target == ".":
            grid[row+1][col],grid[row][col] = grid[row][col],grid[row+1][col]
        elif target != "#":
            if target == "[":
                move_boxes((row+1, col+1),command)
            elif target == "]":
                move_boxes((row+1, col-1),command)
            move_boxes((row+1, col), command)
            grid[row+1][col],grid[row][col] = grid[row][col],grid[row+1][col]
    else:
        return False

def part_one():
    identity = {'#':'#', 'O':'O','.':'.','@':'@'}
    global grid
    grid, commands, bot_pos = parse_input(identity)
    total_gps = 0
    w,h = len(grid[0]), len(grid)
    for c in commands:
        #print("\n",bot_pos,c)
        bot_pos = move_bot(bot_pos, c)
        #for row in grid:
        #    print(''.join(row))
    
    for i,row in enumerate(grid):
        #print(''.join(row))
        for j,col in enumerate(row):
            if col == "O":
                total_gps += i * 100 + j
    #print('-------------------')
    print(total_gps)

def part_two():
    map_changes = {'#':'##', 'O':'[]','.':'..','@':'@.'}
    global grid
    grid, commands, bot_pos = parse_input(map_changes)
    total_gps = 0
    w,h = len(grid[0]), len(grid)
    for c in commands:
        #print("\n",bot_pos,c)
        bot_pos = move_bot(bot_pos, c)
        #for row in grid:
        #    print(''.join(row))
    for i,row in enumerate(grid):
        #print(''.join(row))
        for j,col in enumerate(row):
            if col == "[":
                total_gps += i * 100 + j
    #print('-------------------')
    print(total_gps)

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