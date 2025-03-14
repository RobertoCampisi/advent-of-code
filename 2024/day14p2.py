import math
# Online Python - IDE, Editor, Compiler, Interpreter

width = 101
height = 103


robots = []

with open('input.txt') as f:
    input1 = f.read()
    for line in input1.splitlines():
        pos_str ,vel_str = line.split(' ')
        pos = tuple(map(int,pos_str.split('=')[1].split(',')))
        vel = tuple(map(int,vel_str.split('=')[1].split(',')))
        robots.append({'pos':pos,'vel':vel})

def simulate(r_init,t, verbose):
    r = r_init
    #final time step
    r_end = []
    for robot in r:
        pos_next = ((robot['pos'][0] + robot['vel'][0] * t) % width,(robot['pos'][1] + robot['vel'][1] * t) % height) 
        r_end.append({'pos':pos_next,'vel':robot['vel']})
    r = r_end
    
    grid = [[0 for i in range(width)] for _ in range(height)]
    for robot in r:
        grid[robot['pos'][1]][robot['pos'][0]] += 1
    if verbose:
        for k,row in enumerate(grid):
            temp = ''.join([str(i) for i in row]).replace('0','.')
            if k == math.floor(height/2):
                print(''*width)
            else:
                print(temp[:(math.floor(width/2))] + ' ' + temp[(math.floor(width/2) + 1):])
        print(''*width)
    #calc safety factor
     #binning the robot count
    #quadrants = [0,0,0,0]
    #for robot in r:
    #    if robot['pos'][0] < math.floor(width/2):
    #        if robot['pos'][1] < math.floor(height/2):
    #            quadrants[0] += 1
    #        elif robot['pos'][1] > math.floor(height/2):
    #            quadrants[2] += 1
    #    elif robot['pos'][0] > math.floor(width/2):
    #        if robot['pos'][1] < math.floor(height/2):
    #            quadrants[1] += 1
    #        elif robot['pos'][1] > math.floor(height/2):
    #            quadrants[3] += 1
    #print(quadrants)
    #print(math.prod(quadrants))
    return grid

def highest_column_count(grid):
    highest_adj_column_counts = [0]*len(grid[0])
    adjecent_column_counts = [0]*len(grid[0])
    for row in grid:
        adjecent_column_counts = [ 0 if b == 0 else a for (a,b) in zip(adjecent_column_counts, row)]
        adjecent_column_counts = [sum(x) for x in zip(adjecent_column_counts, row)]
        highest_adj_column_counts = [max(x) for x in zip(highest_adj_column_counts, adjecent_column_counts)]
    return max(highest_adj_column_counts)

best_candidate = 0
a = 101 
c = 14 
hcc = 0
for n in range(10000):
    candidate = highest_column_count(simulate(robots, a*n + c, False))
    if  candidate > hcc:
        hcc = candidate
        best_candidate = a*n+c
    print(n*c,hcc, best_candidate)
    
    
