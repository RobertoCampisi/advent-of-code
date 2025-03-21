with open('input.txt',"r") as f:
    codes = f.read().split('\n')

num_keypad = [['7','8','9'],['4','5','6'],['1','2','3'],[None,'0','A']]
dir_keypad = [[None,'^','A'],['<','v','>']]

def robo_key(c):
    cur_pos = [3,2]
    out = ''
    for ch in c:
        for i,row in enumerate(num_keypad):
            for j,k in enumerate(row):
                if k == ch: 
                    dif_x = j - cur_pos[1] 
                    dif_y = i - cur_pos[0]
                    while dif_x > 0:
                        out += '>'
                        dif_x -= 1
                    while dif_x < 0:
                        if num_keypad[cur_pos[0]][cur_pos[1] + dif_x] == None:
                            while dif_y > 0:
                                out += 'v'
                                dif_y -= 1
                            while dif_y < 0:
                                out  += '^'
                                dif_y += 1
                        out += '<'
                        dif_x += 1
                    while dif_y > 0:
                        out += 'v'
                        dif_y -= 1
                    while dif_y < 0:
                        out  += '^'
                        dif_y += 1
                    out += 'A'
                    cur_pos = [i,j]
    return out

def robo_dir(c):
    cur_pos = [0,2]
    out = ''
    for ch in c:
        for i,row in enumerate(dir_keypad):
            for j,k in enumerate(row):
                if k == ch: 
                    dif_x = j - cur_pos[1] 
                    dif_y = i - cur_pos[0]
                    while dif_x > 0:
                        out += '>'
                        dif_x -= 1
                    while dif_x < 0:
                        if num_keypad[cur_pos[0]][cur_pos[1] + dif_x] == None:
                            while dif_y > 0:
                                out += 'v'
                                dif_y -= 1
                            while dif_y < 0:
                                out  += '^'
                                dif_y += 1
                        out += '<'
                        dif_x += 1
                    while dif_y > 0:
                        out += 'v'
                        dif_y -= 1
                    while dif_y < 0:
                        out  += '^'
                        dif_y += 1
                    out += 'A'
                    cur_pos = [i,j]
    return out
    
print(codes)
res = 0
for code in codes:
    print(code)
    input_code = robo_dir(robo_dir(robo_key(code)))
    print(input_code)
    length_input = len(input_code) 
    constant = int(''.join(filter(str.isdigit,code.lstrip('0'))))
    print(length_input,constant)
    res += length_input * constant
print(res)
