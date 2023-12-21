import sys 
import re
from collections import defaultdict
from collections import deque
from math import lcm

def parse():
    lines = open(sys.argv[1]).read().splitlines()
    mat = defaultdict(lambda: '.')
    for y in range(0, len(lines)):
        for x in range(0, len(lines[0])):
            if lines[y][x] == 'S':
                mat[(x,y)] = 'O'
            else:
                mat[(x,y)] = lines[y][x]
            
    w = len(lines[0])
    h = len(lines)
    return mat, w, h

def get_bounds(matrix, check=lambda map, pos: True):
    ymin = xmin = sys.maxsize
    xmax = ymax = -sys.maxsize
    for (x,y) in matrix.keys():
        if check(matrix, (x,y)):
            xmin = min(xmin, x)
            xmax = max(xmax, x)
            ymin = min(ymin, y)
            ymax = max(ymax, y)
    tl = (xmin, ymin)
    br = (xmax, ymax)
    return (tl, br)

def printm(img):
    tl, br = get_bounds(img)
    for y in range(tl[1], br[1]+1):
        rc = 0
        for x in range(tl[0], br[0]+1):
            print(img[(x,y)] if (x, y) in img else '.', end='')
            rc += 1 if (x, y) in img and img[(x,y)] == 'O' else 0
        print('rc', rc)

def get_os(mat):
    os = []
    for p in mat:
        if mat[p] == 'O':
            os.append(p)
    return os

def count(mat):
    cnt = 0
    for p in mat:
        if mat[p] == 'O':
            cnt += 1
    return cnt

def step(mat):
    startpos = get_os(mat)
    for pos in startpos:
        for dx,dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            mat[pos] = '.'
            if mat[(pos[0]+dx, pos[1]+dy)] in ['.', 'O']:
                mat[(pos[0]+dx, pos[1]+dy)] = 'O'

def part1():
    mat, _, _ = parse()

    for i in range(64):
        step(mat)
#        printm(mat)
   
    print('Part1', count(mat))

def printm2(img, w, h, tl = None, br = None):
    if not tl:
        tl, br = get_bounds(img)
    for y in range(tl[1], br[1]+1):
        rc = 0
        if y % h == 0:
            x = tl[0]
            while x < br[0]+1:
                if x % w == 0:
                    dbgs ='x'+str(x//w)+ 'y'+str(y//h)
                    print('|'+dbgs, end='')
                    x+=len(dbgs)
                else:
                    print('_', end='')
                    x+=1
            print()
        for x in range(tl[0], br[0]+1):
            if x % w == 0:
                print('|', end='')
            if img[(x%w,y%h)] == '#':
                print('#', end='')
            else:
                print(img[(x,y)], end='')
            rc += 1 if (x, y) in img and img[(x,y)] == 'O' else 0
        print()

def step2(mat, w, h):
    startpos = get_os(mat)
    for pos in startpos:
        for dx,dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            mat[pos] = '.'
            if mat[((pos[0]+dx)%w, (pos[1]+dy)%h)] != '#':
                mat[(pos[0]+dx, pos[1]+dy)] = 'O'

def part2():
    mat, w, h = parse()

    saturation_steps = 65
    r = 1
    cycle = 1
    while True:
        step2(mat, w, h)
#        printm2(mat, w, h)
        c = count(mat)
        if cycle == saturation_steps:
            c65 = c
        if cycle == saturation_steps-1:
            c64 = c

        if (cycle-saturation_steps) % w == 0:
            n5 = (r//2+1)*(r//2+1)
            n4 = (r//2)*(r//2)
            if cycle == saturation_steps+w:
                cmagic = (c - (n4*c64 + n5*c65)) / 4
                break
            
            r += 2
        cycle += 1

    r = (26501365-65)//w*2+1

    n5 = (r//2+1)*(r//2+1)
    n4 = (r//2)*(r//2)

    # final pattern consists of "saturated" initial patterns. Some of those have same count of O's as pattern had at steps 64 and 65. 
    # Rest of them have some magic count of O's which was found experimentally. time well spent :)
    pred = (r*r - n5 - n4) * cmagic + n4*c64 + n5*c65
    print("Part2", pred)

part1()
part2()