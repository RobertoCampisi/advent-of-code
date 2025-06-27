import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import my_util functions

def parse_input():
    with open('2016/input/day07.txt','r') as input_file:
        ip_addresses = []
        for address in input_file.read().split('\n'):
            supernets = []
            hypernets = []
            i = 0
            for seq_match in re.finditer(r'\[.*?\]', address):
                supernets.append(address[i:seq_match.start()])
                hypernets.append(address[seq_match.start()+1:seq_match.end()-1])
                i = seq_match.end()
            supernets.append(address[i:])
            ip_addresses.append({'supernets':supernets, 'hypernets':hypernets})
        return ip_addresses

def part_one():
    ip_addresses = parse_input()
    TLS_support_count = 0
    for address in ip_addresses:
        #regex for 'ABBA'
        abba_supernets = [re.search(r'(.)(.)\2\1', seq) for seq in address['supernets']]
        #filter out 'AAAA'
        abba_supernets = [None if m is not None and re.search(r'(.)\1{3}', m.group(0)) else m for m in abba_supernets]
        abba_hypernets = [re.search(r'(.)(.)\2\1', seq) for seq in address['hypernets']]
        abba_hypernets = [None if m is not None and re.search(r'(.)\1{3}', m.group(0)) else m for m in abba_hypernets]
        if any(abba_supernets) and not any(abba_hypernets):
            TLS_support_count += 1
    print(TLS_support_count)

def part_two():
    ip_addresses = parse_input()
    SSL_support_count = 0
    for address in ip_addresses:
        #regex for 'ABA'
        aba_supernets = [re.search(r'(?=((.)(?!\2).\2))', seq) for seq in address['supernets']]
        aba_supernets = [x.group(1) if x is not None else None for x in aba_supernets]
        #filter out 'AAA'
        aba_supernets = [None if m is not None and re.search(r'(.)\1{2}', m) else m for m in aba_supernets]
        aba_supernets = [m for m in filter(lambda x: x is not None, aba_supernets)]
        #regex for 'BAB'
        bab_hypernets = [re.search(r'(?=((.)(?!\2).\2))', seq) for seq in address['hypernets']]
        bab_hypernets = [x.group(1) if x is not None else None for x in bab_hypernets]
        bab_hypernets = [m for m in filter(lambda x: x is not None, bab_hypernets)] 
        print(aba_supernets, bab_hypernets)
        aba_has_bab = [(x[1] + x[0] + x[1]) in bab_hypernets for x in aba_supernets]
        if any(aba_has_bab):
            SSL_support_count += 1
        else:
            print(aba_supernets, bab_hypernets, aba_has_bab)
    print(SSL_support_count)

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