map_changes = {'#':'##', 'O':'[]','.':'..','@':'@.'}

with open('input.txt') as f:
    input1, input2 = f.read().split("\n\n")
 
    #grid = [list(line) for line in input1.splitlines()]
    grid = [list(''.join(map(lambda x: map_changes[x],line))) for line in input1.splitlines()]
    commands = ''.join([i.strip() for i in input2.splitlines()])

def move_bot(pos, command):
    row, col = pos
    if push_boxes(pos, c):
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
        
for i,row in enumerate(grid):
    for j,col in enumerate(row): 
        if grid[i][j] == "@":
            bot_pos = (i,j)
            break

print(bot_pos)

total_gps = 0
w,h = len(grid[0]), len(grid)
for c in commands:
    #print("\n",bot_pos,c)
    bot_pos = move_bot(bot_pos, c)
    #for row in grid:
    #    print(''.join(row))
                
for i,row in enumerate(grid):
    print(''.join(row))
    for j,col in enumerate(row):
        if col == "[":
            total_gps += i * 100 + j
print('-------------------')
print(total_gps)
