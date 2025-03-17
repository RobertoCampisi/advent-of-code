#registers
A = 4
B = 5
C = 6
registers = {0:0,1:1,2:2,3:3,4:0,5:0,6:0,7:'invalid'}

ins_counter = [0]
output = []
final_candidates = []
#operations

def adv(x,reg,ic,out): #opcode 0
    reg[A] = int(reg[A] / 2 ** reg[x])
    ic[0] += 2

def blx(x,reg,ic,out): #opcode 1
    reg[B] = reg[B] ^ x
    ic[0] += 2

def bst(x,reg,ic,out): #opcode 2
    reg[B] = reg[x] % 8
    ic[0] += 2

def jnz(x,reg,ic,out): #opcode 3
    if reg[A] == 0:
        ic[0] += 2
    else:    
        ic[0] = x

def bxc(x,reg,ic,out): #opcode 4
    reg[B] = reg[B] ^ reg[C]
    ic[0] += 2
    
def out(x,reg,ic,out): #opcode 5
    out.append(reg[x]%8)
    ic[0] += 2

def bdv(x,reg,ic,out): #opcode 6
    reg[B] = int(reg[A] / 2 ** reg[x])
    ic[0] += 2

def cdv(x,reg,ic,out): #opcode 7
    reg[C] = int(reg[A] / 2 ** reg[x])
    ic[0] += 2

instruction_set = [adv,blx, bst, jnz, bxc, out, bdv, cdv]

with open("input.txt",'r') as f:
    init, program = f.read().split("\n\n")
    init = init.split("\n")
    #load initial values
    for i in range(3):
        registers[4+i] = int(init[i].split(":")[1])
    instructions = list(map(int,program.split(":")[1].split(",")))

#brute-force does not seems to get there
def find_A(progress):
    for j in range(8):
        #construct A
        attempt = sum([x*8**(k+1) for (x,k) in zip(progress, range(len(progress)))]) + j
        registers[A] = attempt
        registers[B] = 0
        registers[C] = 0
        ins_counter[0] = 0
        output = []
        while(ins_counter[0] < len(instructions)):
            instruction_set[instructions[ins_counter[0]]](instructions[ins_counter[0]+1], registers, ins_counter, output)
            if len(output) > len(instructions):
                break
        #print(attempt, j, output)
        if output == instructions[- len(progress) - 1:]:
            find_A([j] + progress)
            if len(output) == len(instructions):
                final_candidates.append(attempt)
find_A([])
print(min(final_candidates))
