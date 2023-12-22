import sys 
import re
from collections import defaultdict
import itertools
import copy

def parse():
    lines = open(sys.argv[1]).read().splitlines()
    bricks = []
    for l in lines:
        m = re.search(r'(\d*),(\d*),(\d*)~(\d*),(\d*),(\d*)', l)
        assert(m)
        bricks.append([[int(m.group(1)), int(m.group(2)), int(m.group(3))], [int(m.group(4)), int(m.group(5)), int(m.group(6))]])

    bricks = sorted(bricks, key=lambda b: min(b[0][2], b[1][2]))
    return bricks

def get_bounds(matrix):
    ymin = xmin = sys.maxsize
    xmax = ymax = -sys.maxsize
    for (x,y, _) in matrix.keys():
        xmin = min(xmin, x)
        xmax = max(xmax, x)
        ymin = min(ymin, y)
        ymax = max(ymax, y)
    tl = (xmin, ymin)
    br = (xmax, ymax)
    return (tl, br)

def printm(img, yside):
    tl, br = get_bounds(img)
    d1 = 0 if not yside else 1
    d2 = 1 if not yside else 0
    for z in range(10, -1, -1):
        for a in range(tl[d1], br[d1]+1):
            has = False
            for b in range(tl[d2], br[d2]+1):
                chk = (a, b, z) if not yside else (b, a, z)
                if chk in img:
                    has = True
                    break
            if has:
                print(img[chk], end='')
            else:
                print('.', end='')
        print(", z", z)
    print(tl, br)

def fall(bricks):
    fallcnt = 0
    world = to_world(bricks)
    for i,b in enumerate(bricks):
        fallz = 0
        while True:
            ok = True
            for x, y, z in itertools.product(range(b[0][0], b[1][0]+1), range(b[0][1], b[1][1]+1), range(b[0][2], b[1][2]+1)):
                tryz = z - fallz - 1
                if world[(x, y, tryz)] not in ['.', str(i)] or tryz <= 0:
                    ok = False
                    break
            if not ok:
                break
            fallz += 1
        if fallz > 0:
            for x, y, z in itertools.product(range(b[0][0], b[1][0]+1), range(b[0][1], b[1][1]+1), range(b[0][2], b[1][2]+1)):
                world[(x,y,z)] = '.'
            b[0][2] -= fallz
            b[1][2] -= fallz
            for x, y, z in itertools.product(range(b[0][0], b[1][0]+1), range(b[0][1], b[1][1]+1), range(b[0][2], b[1][2]+1)):
                world[(x,y,z)] = str(i)
            fallcnt += 1
    return fallcnt

def to_world(bricks):
    world = defaultdict(lambda:'.')
    for i, b in enumerate(bricks):
        for x, y, z in itertools.product(range(b[0][0], b[1][0]+1), range(b[0][1], b[1][1]+1), range(b[0][2], b[1][2]+1)):
            world[(x,y,z)] = str(i)
    return world    

def printb(bricks):
    world = to_world(bricks)               
    printm(world, False)
    printm(world, True)

def part1():
    bricks = parse()

#    printb(bricks)
    fall(bricks)
#    printb(bricks)
    cnt = 0
    for b in range(len(bricks)):
        cbricks = copy.deepcopy(bricks)
        nbricks = cbricks[0:b]+cbricks[b+1:]
        if fall(nbricks) == 0:
            cnt += 1
    print('Part1',cnt)

def part2():
    bricks = parse()
    fall(bricks)
    cnt = 0
    for b in range(len(bricks)):
        cbricks = copy.deepcopy(bricks)
        nbricks = cbricks[0:b]+cbricks[b+1:]
        cnt += fall(nbricks)
    print('Part2',cnt)

part1()
part2()