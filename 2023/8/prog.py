import sys 
from collections import defaultdict
from math import gcd

def parse():
    lines = open(sys.argv[1]).read().splitlines()
    cmds = lines[0]

    map = {}
    for l in lines[2:]:
        a = l.split(' = ')
        fr = a[0]
        to1 = a[1][1:4]
        to2 = a[1][6:9]
        map[fr] = (to1, to2)
    return cmds, map

def part1():
    cmds, map = parse()
    i = 0
    node = 'AAA'
    steps = 0
    while True:
        steps += 1
        if i == len(cmds):
            i = 0
        instr = cmds[i]
        i += 1
        if instr == 'L':
            node = map[node][0]
        else:
            node = map[node][1]
        if node == 'ZZZ':
            break
    print('Part1', steps)

def array_lcm(a):
    lcm = 1
    for i in a:
        lcm = lcm*i//gcd(lcm, i)
    return lcm

def part2():
    cmds, map = parse()
    start = []
    for k in map.keys():
        if k[2] == 'A':
            start.append(k)

    steps = 0
    i = 0
    nodes = start
    period = [0 for i in range(len(nodes))]
    while True:
        steps += 1
        if i == len(cmds):
            i = 0
        instr = cmds[i]
        i += 1
        allz = True
        allperiod = True
        for n in range(len(nodes)):
            node = nodes[n]
            if instr == 'L':
                node = map[node][0]
            else:
                node = map[node][1]
            nodes[n] = node
            if node[2] != 'Z':
                allz = False
            else:
                if period[n] == 0:
                    period[n] = steps
            if period[n] == 0:
                allperiod = False
        if allperiod:
            break
        if allz:
            break
    print('steps', steps, 'per', period)
    ret = array_lcm(period)
    print('Part2', ret)

part1()
part2()