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

def simulate(r_init,t):
    r = r_init
    for _ in range(t):
        #next time step
        r_next = []
        for robot in r:
            pos_next = ((robot['pos'][0] + robot['vel'][0]) % width,(robot['pos'][1] + robot['vel'][1]) % height) 
            r_next.append({'pos':pos_next,'vel':robot['vel']})
        r = r_next
    
    grid = [[0 for i in range(width)] for _ in range(height)]
    for robot in r:
        grid[robot['pos'][1]][robot['pos'][0]] += 1
    for k,row in enumerate(grid):
        temp = ''.join([str(i) for i in row]).replace('0','.')
        if k == math.floor(height/2):
            print(''*width)
        else:
            print(temp[:(math.floor(width/2))] + ' ' + temp[(math.floor(width/2) + 1):])
    print(''*width)
    #calc safety factor
     #binning the robot count
    quadrants = [0,0,0,0]
    for robot in r:
        if robot['pos'][0] < math.floor(width/2):
            if robot['pos'][1] < math.floor(height/2):
                quadrants[0] += 1
            elif robot['pos'][1] > math.floor(height/2):
                quadrants[2] += 1
        elif robot['pos'][0] > math.floor(width/2):
            if robot['pos'][1] < math.floor(height/2):
                quadrants[1] += 1
            elif robot['pos'][1] > math.floor(height/2):
                quadrants[3] += 1
    print(quadrants)
    print(math.prod(quadrants))
        
simulate(robots, 100)
