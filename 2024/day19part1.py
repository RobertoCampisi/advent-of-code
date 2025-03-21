with open('input.txt',"r") as f:
    towels, designs = f.read().split('\n\n')
    towels = towels.split(", ")
    designs = designs.split("\n")

#dictionary to store possible towel arrangements
towel_mem = set()

def rec(d, towels):
    if d in towel_mem:
        return True
    #terminate
    if d == '':
        return True
    for t in towels:
        if d.startswith(t):
            if rec(d[len(t):], towels):
                towel_mem.add(d)
                return True
    return False
    
res = 0             
for i,d in enumerate(designs):
    if rec(d,towels):
        res += 1

print(res)
