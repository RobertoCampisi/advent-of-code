def read_input(lines):
    out = []
    for line in lines:
        temp = line.split(':')[1].strip().split(',')
        out.append(int(temp[0][2:]) + int(temp[1][3:])*1j)
    return out

#solve lowest cost for k*a + l*b = c, where cost = 3*k + l    
def solve(a,b,c):
    equations = [[a.real, b.real, -c.real], [a.imag,b.imag,-c.imag]]
    workspace = []
    for eq in range(len(equations)):
        index = list(filter(lambda x: x[0] != 0, equations))[0]
        workspace.append([-1.0*i/index[0] for i in index[1:]])
        equations.remove(index)
        for i in equations:
            for j in range(len(workspace[-1])):
                    i[j+1]+=i[0]*workspace[-1][j]
            i.pop(0)
    workspace.reverse()
    an=[workspace[0][0]]
    for i in range(1,len(workspace)):
        tmpans=workspace[i][-1]
        for j in range(len(workspace[i])-1):
            tmpans+=workspace[i][j]*an[-1-j]
        an.append(tmpans)
    return round(an[1]) * 3 + round(an[0]) if abs(an[0] - round(an[0])) < 0.001 and abs(an[1] - round(an[1])) < 0.001 else 0

machines = open("input.txt").read().split('\n\n')
minimum_tokens = 0
for machine in machines:
    a, b, c = read_input(machine.split('\n')[0:3])
    c = c+ (10000000000000 + 10000000000000j)
    res = solve(a,b,c)
    minimum_tokens += res
print(minimum_tokens)
