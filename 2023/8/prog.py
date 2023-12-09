import sys
from math import lcm

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
    print(map)
    while True:
        steps += 1
        instr = cmds[i]
        i = i + 1 if i < len(cmds) - 1 else 0
        node = map[node][0] if instr == 'L' else  map[node][1]
        if node == 'ZZZ':
            break
    print('Part1', steps)

def part2():
    cmds, map = parse()
    start = [i for i in map.keys() if i[2] == 'A']
    steps = 0
    i = 0
    nodes = start
    period = [0 for i in range(len(nodes))]
    while True:
        steps += 1
        instr = cmds[i]
        i = i + 1 if i < len(cmds) - 1 else 0
        allz = True
        allperiod = True
        for n in range(len(nodes)):
            nodes[n] = map[nodes[n]][0] if instr == 'L' else  map[nodes[n]][1]
            if nodes[n][2] != 'Z':
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
    ret = lcm(*period)
    print('Part2', ret)

part1()
part2()