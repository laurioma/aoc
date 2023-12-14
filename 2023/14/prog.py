import sys 
from collections import defaultdict

def printm(matrix):
    for r in matrix:
        for c in r:
            print(c, end='')
        print("")

def tiltd(matrix, dir): 
    if dir == 'N' or dir == 'S':
        rngy = range(len(matrix)) if dir == 'N' else reversed(range(len(matrix)))
        dy = -1 if dir == 'N' else 1
        for y in rngy:
            for x in range(len(matrix[0])):
                if matrix[y][x] == 'O':
                    yy = y + dy
                    while 0 <= yy < len(matrix) and matrix[yy][x] == '.':
                        matrix[yy][x] = 'O'
                        matrix[yy - dy][x] = '.'
                        yy += dy
    elif dir == 'E' or dir == 'W':
        dx = -1 if dir == 'W' else 1
        for y in range(len(matrix)):
            # re-evaluate since range() returns range object but reversed(range()) returns iterator..
            rngx = range(len(matrix[0])) if dir == 'W' else reversed(range(len(matrix[0])))
            for x in rngx:
                if matrix[y][x] == 'O':
                    xx = x + dx
                    while 0 <= xx < len(matrix[0]) and matrix[y][xx] == '.':
                        matrix[y][xx] = 'O'
                        matrix[y][xx - dx] = '.'
                        xx += dx

def calcload(matrix):
    sum = 0
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == 'O':
                sum += len(matrix) - y
    return sum

def part1():
    lines = open(sys.argv[1]).read().splitlines()
    matrix = [list(row) for row in lines]; w=len(matrix[0]); h=len(matrix)
    tiltd(matrix, 'N')
#    printm(matrix)
    print('Part1', calcload(matrix))


def part2():
    lines = open(sys.argv[1]).read().splitlines()
    matrix = [list(row) for row in lines]; w=len(matrix[0]); h=len(matrix)
    loadc = defaultdict(list)
    per_mod_load = defaultdict(lambda: defaultdict(list))
    for cycle in range(1, 500):
        for dir in ['N', 'W', 'S', 'E']:
            tiltd(matrix, dir)
        load = calcload(matrix)
        loadc[load].append(cycle)
        if len(loadc[load]) > 1:
            per = loadc[load][-1] - loadc[load][-2]
            cycmod = cycle % per
            per_mod_load[per][cycmod].append(load)
    max_per_cnt = 0
    likely_per = 0
    for per in per_mod_load:
        per_cnt = sum([len(per_mod_load[per][mod]) for mod in per_mod_load[per]])
        if per_cnt > max_per_cnt:
            max_per_cnt = per_cnt
            likely_per = per
    mod = 1000000000 % likely_per
    print('Part2', per_mod_load[likely_per][mod][0])

part1()
part2()
