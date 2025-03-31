maze = dict()

with open('example.txt') as f:
    input = f.read()
    w, h = len(input.split('\n')[0]), len(input.split('\n'))
    for j,row in enumerate(input.split('\n')):
        for i,ch in enumerate(list(row)):
            maze[i+j*1j] = 1 if ch == '#' else 0

start = 1+(h-2)*1j
end = (w-2)+1j

edges = []
nodes = []
visited = set()

nodes.append((start,1))
visited.add(start)

def prance(grid, start, d):
    queue = [(start,d)]
    while len(queue) > 0:
        pos, old_d = queue.pop(0) 
        #adjecent = list(filter(lambda x: x in grid and grid[x] != 1, [pos+1,pos-1,pos+1j,pos-1j]))
        #print(adjecent)
        for d in [1,-1,1j,-1j]:
            i = 1
            base_cost = 0 if old_d == d else 1000
            while grid[pos + d*i] != 1 and grid[pos + d*i] not in visited:
                i += 1
                visited.add(pos+d*i)
            if i > 1:
                nodes.append((pos+d*(i-1),d))
                edges.append(((pos,d),(pos+d*(i-1)),base_cost+(i-1)))
                queue.append((pos+d*(i-1),d))
        print(queue)

prance(maze,start,1)    
print(nodes)
print(edges)
print(visited)
#print(is_node(maze,start))
