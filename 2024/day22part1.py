from functools import lru_cache

def sim(init, d):
    n = init
    while d > 0:
        n = next(n)
        d -= 1
    return n

@lru_cache(maxsize=None)
def next(n):
    n = (n ^ n << 6) % (1 << 24)
    n = (n ^ n >> 5) % (1 << 24)
    n = (n ^ n << 11)% (1 << 24)
    return n

print(sum(sim(int(n),2000) for n in open("input.txt")))
