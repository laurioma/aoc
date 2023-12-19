import sys 
import re
from collections import defaultdict

def parse():
    a = open(sys.argv[1]).read().split('\n\n')
    rulesl = a[0].splitlines() 
    partsl = a[1].splitlines() 
    rules = {}
    for r in rulesl:
        name, rem = r.split('{')
        rr = rem[:-1].split(',')
        ruleset = []
        for rrr in rr:
            m = re.search(r'(.*)([<>])(\d*):(.*)', rrr)
            if m:
                ruleset.append([m.group(1), m.group(2), int(m.group(3)), m.group(4)])
            else:
                ruleset.append([rrr])
        rules[name] = ruleset
    
    parts=[]
    for p in partsl:
        pp = p[1:-1].split(',')
        partp={}
        for ppp in pp:
            k, v = ppp.split('=')
            partp[k] = int(v)
        parts.append(partp)
    return rules, parts

def chec_part(rules, p):
    rulen = 'in'
    while True:
        ruleset = rules[rulen]
        for rr in ruleset:
            if len(rr) == 1:
                if rr[0] == 'A' or rr[0] == 'R':
                    return rr[0] == 'A'            
                else:
                    rulen = rr[0]
                break
            else:
                rating = p[rr[0]]
                op = rr[1]
                cmpv = rr[2]
                if op == '<':
                    if rating < cmpv:
                        if rr[3] == 'A' or rr[3] == 'R':
                            return rr[3] == 'A'   
                        else:
                            rulen = rr[3]
                        break
                else:
                    assert(op == '>'), 'op'
                    if rating > cmpv:
                        if rr[3] == 'A' or rr[3] == 'R':
                            return rr[3] == 'A'
                        else:
                            rulen = rr[3]
                        break                            

def part1():
    rules, parts = parse()
    accept=[]
    reject=[]
    for p in parts:
        if chec_part(rules, p):
            accept.append(p)
        else:
            reject.append(p)
    res = 0
    for a in accept:
        res += a['x'] + a['m'] + a['a'] + a['s']
    print('Part1', res)

def cnt(arr, idx):
    if idx == 0:
        return arr[idx]
    else:
        return arr[idx] - arr[idx-1]

def part2():
    rules, _ = parse()
    val_ranges = defaultdict(list)
    MAXV = 4000
    for r in rules:
        for rr in rules[r]:
            if len(rr) > 1:
                if rr[1] == '<':
                    val_ranges[rr[0]].append(rr[2]-1)
                else:
                    val_ranges[rr[0]].append(rr[2])
    for v in val_ranges:
        val_ranges[v] = sorted(val_ranges[v])
        val_ranges[v].append(MAXV)

    res = 0
    i = 0
    for xi, x in enumerate(val_ranges['x']):
        for mi, m in enumerate(val_ranges['m']):
            for ai, a in enumerate(val_ranges['a']):
                for si, s in enumerate(val_ranges['s']):
                    part = {'x': x, 'm': m, 'a': a, 's': s}
                    i+=1
                    if i % 1000000 == 0:
                        print(i)
                    if chec_part(rules, part):
                        xc = cnt(val_ranges['x'], xi)
                        mc = cnt(val_ranges['m'], mi)
                        ac = cnt(val_ranges['a'], ai)
                        sc = cnt(val_ranges['s'], si)
                        res += xc * mc * ac *sc

    print('Part2', res)

part1()
part2()