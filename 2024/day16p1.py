maze = []

with open('example.txt') as f:
    input = f.read()
    maze = [list(row) for row in input.split('\n')]
#directions: E, S, W, N
directions = [(0,1),(1,0),(0,-1),(-1,0)]

print(maze)

start = (1,len(maze)-2)
end = (len(maze[0])-2,1)

edges = []
nodes = []
visited = []

nodes.append([start,0])

def is_node(grid,pos):
    print(pos[1])
    if grid[pos[1]][pos[0]] == '#':
        return False
    adj = []
    for d in directions:
        adj.append(grid[pos[1]+d[1]][pos[0]+d[0]])
    paths = len(list(filter(lambda x: x == '.', adj)))
    if paths == 1:
        return False
    if paths == 2:
        if adj[0] == '.' and adj[2] == '.':
            return False
        elif adj[1] == '.' and adj[3] == '.':
            return False
        else:
            return True
    else: 
        return True

def prance(grid, pos, d):
    adjecent = []
    for direction in directions:
        adjecent.append(grid[pos[1]+direction[1]][pos[0]+direction[0]])
    for i,adj in enumerate(adjecent):
        if adj == '.':
            distance = 1
            while not is_node(grid, (pos[1] + directions[i][1] * d, pos[0] + directions[i][0] * d)):
                if grid[pos[1] + directions[i][1] * d][pos[0] + directions[i][0] * d] != '#':
                    distance += 1
                else:
                    break
            if grid[pos[1] + directions[i][1] * d][pos[0] + directions[i][0] * d] != '#':
                nodes.append([(pos[0] + directions[i][0],pos[1] + directions[i][1]),i])
                edges.append(distance + (1000 if d != i else 0))

prance(maze,start,0)    
print(nodes)
print(edges)
#print(is_node(maze,start))
