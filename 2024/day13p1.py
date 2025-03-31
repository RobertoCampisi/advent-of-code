def read_input(lines):
    out = []
    for line in lines:
        temp = line.split(':')[1].strip().split(',')
        out.append(int(temp[0][2:]) + int(temp[1][3:])*1j)
    return out

#solve lowest cost for k*a + l*b = c, where cost = 3*k + l    
def solve(a,b,c):
    res = dict()
    #brute force
    for k in range(100):
        for l in range(100):
            if k*a + l*b == c:
                res[(k,l)] = 3*k + l
    return min(res.values()) if len(res) > 0 else 0

machines = open("input.txt").read().split('\n\n')
minimum_tokens = 0
for machine in machines:
    a, b, c = read_input(machine.split('\n')[0:3])
    minimum_tokens += solve(a,b,c)
print(minimum_tokens)
