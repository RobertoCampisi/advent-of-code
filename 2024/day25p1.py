keys = []
locks = []
for c in open("input.txt").read().split("\n\n"):
    rows = c.split('\n')
    if rows[0] == '.....': #keys
        keys.append(list(map(sum, zip(*[[1 if x == '#' else 0 for x in rows[i]] for i in range(1,6)]))))
    if rows[0] == '#####': #locks
        locks.append(list(map(sum, zip(*[[1 if x == '#' else 0 for x in rows[i]] for i in range(1,6)]))))

res = 0        
for k in keys:
    for l in locks:
        if len(list(filter(lambda x: x > 5, [sum(x) for x in zip(k, l)]))) == 0:
            res += 1
print(res)
            
