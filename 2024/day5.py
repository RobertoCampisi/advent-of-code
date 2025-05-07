import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2024/input/day5.txt','r') as input_file:
        lines = input_file.read().strip().split("\n")

        rules = []
        prints = []
        i = 0
        while i < len(lines):
            while i < len(lines) and not lines[i] == "":
                b, a = list(map(int, lines[i].split('|')))
                rules.append((b, a))
                i += 1
            break
        while i < len(lines):
            while i < len(lines) and not lines[i] == "":
                pages = list(map(int, lines[i].split(',')))
                prints.append(pages)
                i += 1
            i += 1

        rule_dict = dict()

        for (a, b) in rules:
            current = []
            if b in rule_dict:
                current = rule_dict[b]
            current.append(a)
            rule_dict[b] = current

        return prints, rule_dict

def right_order(ps, rs):
    constraints = []
    for page in ps:
        # print(constraints)
        if page in constraints:
            return False
        if page in rs:
            constraints += rs[page]
    return True

def out_order_hit(ps, rs):
    c = []
    for page in ps:
        for i in range(len(c)):
            if page in c[i][1]:
                return c[i][0],page
        if page in rs:
            c.append((page,rs[page]))
    return None

def reorder(ps, rs, hit):
    current_hit = hit
    while current_hit is not None:
        k = [0,0]
        for j in range(len(ps)):
            if ps[j] == current_hit[0]:
                k[0] = j
            elif ps[j] == current_hit[1]:
                k[1] = j
        #swap
        ps[k[0]], ps[k[1]] = current_hit[1], current_hit[0]
        #print('new pages', ps)
        current_hit = out_order_hit(ps, rs)
    return ps

def part_one():
    prints, rule_dict = parse_input()
    total = 0
    for pages in prints:
        valid = right_order(pages, rule_dict)
        # print(is_valid)
        if valid:
            # add midpoint to total
            total += pages[len(pages) // 2]
    print(total)

def part_two():
    prints, rule_dict = parse_input()
    total = 0
    for pages in prints:
        hit = out_order_hit(pages, rule_dict)
        if hit is not None:
            new_order = reorder(pages, rule_dict, hit)
            # add midpoint to total
            total += new_order[len(pages) // 2]
    print(total)

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