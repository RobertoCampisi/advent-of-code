from functools import lru_cache

keys = []
locks = []
for c in open("input.txt").read().split("\n\n"):
    rows = c.split('\n')
    pin_heights = [0,0,0,0,0]
    if rows[0] == '.....': #keys
        for i in range(1,6):
            for j in range(5):
                if rows[i][j] == '#':
                    pin_heights[j] += 1
        keys.append(pin_heights)
    if rows[0] == '#####': #locks
        for i in range(1,6):
            for j in range(5):
                if rows[i][j] == '#':
                    pin_heights[j] += 1
        locks.append(pin_heights)
        
res = 0      
for k in keys:
    for l in locks:
        if len(list(filter(lambda x: x > 5, [sum(x) for x in zip(k, l)]))) == 0:
            res += 1
print(res)
            
