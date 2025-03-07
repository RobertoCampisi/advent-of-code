with open('input.txt') as f:
    input1, input2 = f.read().split("\n\n")
 
    grid = [list(line) for line in input1.splitlines()]
    commands = ''.join([i.strip() for i in input2.splitlines()])

def move_bot(pos, command):
    row, col = pos
    if command == "<":
        target = grid[row][col-1]
        if target == ".":
            grid[row][col-1] = "@"
            grid[row][col] = "."
            col -= 1
        elif target == "O":
            if move_boxes(pos, c):
                grid[row][col-1] = "@"
                grid[row][col] = "."
                col -= 1
    elif command == ">":
        target = grid[row][col+1]
        if target == ".":
            grid[row][col+1] = "@"
            grid[row][col] = "."
            col += 1
        elif target == "O":
            if move_boxes(pos, c):
                grid[row][col+1] = "@"
                grid[row][col] = "."
                col += 1
    elif command == "^":
        target = grid[row-1][col]
        if target == ".":
            grid[row-1][col] = "@"
            grid[row][col] = "."
            row -= 1
        elif target == "O":
            if move_boxes(pos, c):
                grid[row-1][col] = "@"
                grid[row][col] = "."
                row -= 1
    elif command == "v":
        target = grid[row+1][col]
        if target == ".":
            grid[row+1][col] = "@"
            grid[row][col] = "."
            row += 1
        elif target == "O":
            if move_boxes(pos, c):
                grid[row+1][col] = "@"
                grid[row][col] = "."
                row += 1
    return (row, col)
    
def move_boxes(pos,command):
    row, col = pos
    if command == "<":
        target = grid[row][col-1]
        if target == ".":
            return True
        elif target == "#":
            return False
        else:
            if move_boxes((row, col-1), command):
                grid[row][col-2],grid[row][col-1] = grid[row][col-1],grid[row][col-2]
                return True
            else:
                return False
    elif command == ">":
        target = grid[row][col+1]
        if target == ".":
            return True
        elif target == "#":
            return False
        else:
            if move_boxes((row, col+1), command):
                grid[row][col+2],grid[row][col+1] = grid[row][col+1],grid[row][col+2]
                return True
            else:
                return False
    elif command == "^":
        target = grid[row-1][col]
        if target == ".":
            return True
        elif target == "#":
            return False
        else:
            if move_boxes((row-1, col), command):
                grid[row-2][col],grid[row-1][col] = grid[row-1][col],grid[row-2][col]
                return True
            else:
                return False
    elif command == "v":
        target = grid[row+1][col]
        if target == ".":
            return True
        elif target == "#":
            return False
        else:
            if move_boxes((row+1, col), command):
                grid[row+2][col],grid[row+1][col] = grid[row+1][col],grid[row+2][col]
                return True
            else:
                return False
    else:
        return False
        
for i,row in enumerate(grid):
    for j,col in enumerate(row): 
        if grid[i][j] == "@":
            bot_pos = (i,j)
            break

print(bot_pos)

total_gps = 0
for c in commands:
    print("\n",bot_pos,c)
    bot_pos = move_bot(bot_pos, c)
    for row in grid:
        print(''.join(row))
                
for i,row in enumerate(grid):
    for j,col in enumerate(row):
        if col == "O":
            total_gps += i * 100 + j
print('-------------------')
print(total_gps)
