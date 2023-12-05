import sys 
from collections import defaultdict

def checkchar(x,y,lines):
    for i in range(-1,2):
        for j in range(-1,2):
            yy = y + i
            xx = x + j
            if yy < 0 or yy >= len(lines):
                continue
            if xx < 0 or xx >= len(lines[yy]):
                continue
            if lines[yy][xx] != '.' and not lines[yy][xx].isdigit():
                return True
    return False

def hasstar(x,y,lines):
    for i in range(-1,2):
        for j in range(-1,2):
            yy = y + i
            xx = x + j
            if yy < 0 or yy >= len(lines):
                continue
            if xx < 0 or xx >= len(lines[yy]):
                continue
            if lines[yy][xx] == '*':
                return (xx,yy)
    return False

def part1():
    lines = open(sys.argv[1]).read().splitlines()
    sum = 0
    for y,l in enumerate(lines):
        num = ''
        haschar=False
        for x,c in enumerate(l):
            if c.isdigit():
                if not haschar:
                    haschar=checkchar(x,y,lines)
                num += c
            if not c.isdigit() or x == len(l)-1:
                if num != '':
                    if haschar:
                        sum += int(num)
                haschar = False
                num = ''
    print('Part1', sum)

def part2():
    lines = open(sys.argv[1]).read().splitlines()

    starnums = defaultdict(list)
    for y,l in enumerate(lines):
        num = ''
        starcoords = None
        for x,c in enumerate(l):
            if c.isdigit():
                if not starcoords:
                    starcoords=hasstar(x,y,lines)
                num += c
            if not c.isdigit() or x == len(l)-1:
                if num != '':
                    if starcoords:
                        starnums[starcoords].append(int(num))
                num = ''
                starcoords = None
        sum = 0
        for a in starnums:
            if len(starnums[a]) == 2:
                sum += starnums[a][0] * starnums[a][1]
    print('Part2', sum)

part1()
part2()