import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    #inner function
    def read_machine(lines):
        out = []
        for line in lines:
            temp = line.split(':')[1].strip().split(',')
            out.append(int(temp[0][2:]) + int(temp[1][3:])*1j)
        return out
    with open('2024/input/day13.txt','r') as input_file:
        return [read_machine(machine.split('\n')[0:3]) for machine in input_file.read().split('\n\n')]
            

#naive bruteforce solve lowest cost for k*a + l*b = c, where cost = 3*k + l    
def solve_bruteforce(a,b,c):
    res = dict()
    #brute force
    for k in range(100):
        for l in range(100):
            if k*a + l*b == c:
                res[(k,l)] = 3*k + l
    return min(res.values()) if len(res) > 0 else 0

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
    ans=[workspace[0][0]]
    for i in range(1,len(workspace)):
        tmpans=workspace[i][-1]
        for j in range(len(workspace[i])-1):
            tmpans+=workspace[i][j]*ans[-1-j]
        ans.append(tmpans)
    return round(ans[1]) * 3 + round(ans[0]) if abs(ans[0] - round(ans[0])) < 0.001 and abs(ans[1] - round(ans[1])) < 0.001 else 0

def part_one():
    minimum_tokens = 0
    for machine in parse_input():
        minimum_tokens += solve(*machine)
    print(minimum_tokens)


def part_two():
    minimum_tokens = 0
    for machine in parse_input():
        a, b, c = machine
        c = c+ (10000000000000 + 10000000000000j)
        minimum_tokens += solve(a, b, c)
    print(minimum_tokens)

#simple benchmark function.
def benchmark(func, n):
    from time import time_ns
    start = time_ns() // 1_000 #microseconds
    sys.stdout = None  # bit hacky but it works
    for i in range(0, int(n)):
        globals()[func]()
    sys.stdout = sys.__stdout__ #restore stdout
    end = time_ns() // 1_000 #microseconds
    print((end - start) / int(n) / 1000, end='')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        globals()[sys.argv[1]]()
    elif len(sys.argv) > 2:
        globals()[sys.argv[1]](*sys.argv[2:])
    else:
        raise RuntimeError