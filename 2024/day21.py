from functools import lru_cache

with open('input.txt',"r") as f:
    codes = f.read().split('\n')

#compressed keypads into 1 by replacing ^ by 0
keypad = '789456123 0A<v>'

def path(ss):
    (y,x), (Y,X) = [divmod(keypad.find(t), 3) for t in ss]
    #construct seq
    Seq = '>' * (X - x) + 'v' * (Y - y) + '0' * (y - Y) + '<' * (x - X)
    #panic check (3,0): if so, reverse path order
    return Seq if (3,0) in [(y,X), (Y,x)] else Seq[::-1] 

@lru_cache(maxsize=None)
def length(S, d):
    if d < 0: return len(S)+1
    return sum(length(path(subseq), d-1) for subseq in zip('A' + S, S + 'A'))
    
for r in 2, 25:
    print(sum(int(Seq[:3]) * length(Seq[:3], r) for Seq in codes))
