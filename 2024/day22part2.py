from functools import lru_cache

def sim(init, d):
    n = init
    delta_list, seen = [(n % 10, None)], set()
    while d > 0:
        n = next(n)
        d -= 1
        delta_list.append((n % 10, (n % 10) - delta_list[-1][0]))
        if len(delta_list) > 4:
            seq = tuple([delta_list[-j][1] for j in range(1,5)])
            if seq not in seen:
                seen.add(seq)
                sequences[seq] = sequences[seq] + [n % 10] if seq in sequences else [n % 10]
    return n

@lru_cache(maxsize=None)
def next(n):
    n = (n ^ n << 6) % (1 << 24)
    n = (n ^ n >> 5) % (1 << 24)
    n = (n ^ n << 11)% (1 << 24)
    return n

sequences = {}
for n in open("input.txt"):
    sim(int(n),2000) 

print(max([sum(sequence) for sequence in sequences.values()]))
