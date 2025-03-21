with open('input.txt',"r") as f:
    towels, designs = f.read().split('\n\n')
    towels = towels.split(", ")
    designs = designs.split("\n")

#dictionary to store possible towel arrangements and known ways
towel_mem = dict()

def rec(d, towels):
    if d in towel_mem:
        return towel_mem[d]
    #terminate
    if d == '':
        return 1
    total = 0
    for t in towels:
        if d.startswith(t):
            total += rec(d[len(t):], towels)
    towel_mem[d] = total
    return total
    
res = 0             
for i,d in enumerate(designs):
    n = rec(d,towels)
    res += n

print(res)
