class Node:
    def __init__(self, pos, par=None):
        self.position = pos
        self.parent = par
        self.g = 0
        self.h = 0
        self.f = self.g + self.h
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __eq__(self, other):
        return self.position == other.position
    
    def __str__(self):
        return f'{self.position}, g={self.g}, h={self.h}, f={self.f}'

def get_neighbors(grid, pos):
    return list(filter(lambda x: x in grid and grid[x] != 1, [pos+1,pos-1,pos+1j,pos-1j]))

def get_dist(p1, p2):
    return abs(p1.real - p2.real) + abs(p1.imag - p2.imag)

def astar(grid, start, goal):
    open_set = [Node(start)]
    closed_set = set()
    while open_set:
        current_node = open_set.pop(0)
        closed_set.add(current_node.position)
        
        if current_node.position == goal:
            path = []
            current = current_node.parent
            while current is not None:
                path.append(current.position)
                current = current.parent
            return list(reversed(path))
        
        for n in get_neighbors(grid, current_node.position):
            if n in closed_set:
                continue
            new_g = current_node.g + 1
            neighbor_node = Node(n, current_node)
            if neighbor_node in open_set:
                if new_g >= neighbor_node.g:
                    continue
            neighbor_node.g = new_g
            neighbor_node.h = get_dist(n,goal)
            neighbor_node.f = neighbor_node.g + neighbor_node.h
            open_set.append(neighbor_node)
        open_set.sort()
    return None


racetrack = {}
with open("example.txt",'r') as f:
    start = 0
    end = 0
    lines = f.read().split("\n")
    h, w = len(lines), len(lines[0])
    for j,line in enumerate(lines):
        for i in range(len(line)):
            if line[i] == 'S':
                start = i+j*1j
            if line[i] == 'E':
                end = i+j*1j
            if line[i] == '#':
                racetrack[i+j*1j] = 1
            else:
                racetrack[i+j*1j] = 0

    base_len = len(astar(racetrack, start, end))
    print(base_len) 
    for j in range(1,h-1):
        for i in range(1,w-1):
            for d in {1,-1,1j,-1j}:
                
