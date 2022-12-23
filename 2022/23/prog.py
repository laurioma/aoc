import sys
from collections import defaultdict
import itertools

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
        for x in range(tl[0], br[0]+1):
            print(img[(x,y)] if (x, y) in img else '.', end='')
        print("")

DIR_N=0
DIR_S=1
DIR_W=2
DIR_E=3

def nextdir(dir):
    return (dir+1)%4

def round(map, dir):
    consider={}
    tl, br = get_bounds(map)
    for y, x in itertools.product(range(tl[1], br[1]+1), range(tl[0], br[0]+1)):
        if (x,y) in map and map[(x,y)] =='#':
            consider_dir=dir
            hasothers = False
            for dy, dx in itertools.product(range(-1, 2), range(-1, 2)):
                if dx == 0 and dy == 0:
                    continue
                chkx = x + dx
                chky = y + dy
                if (chkx,chky) in map and map[(chkx,chky)]=='#':
                    hasothers = True
                    break

            if not hasothers:
                continue

            cdest = None
            for _ in range(4):
                if consider_dir == DIR_N:
                    if map[(x-1,y-1)] == '.'and map[(x,y-1)] == '.' and map[(x+1,y-1)] == '.':
                        cdest = (x, y-1)
                        break
                elif consider_dir == DIR_S:
                    if map[(x-1,y+1)] == '.'and map[(x,y+1)] == '.' and map[(x+1,y+1)] == '.':
                        cdest = (x, y+1)
                        break
                elif consider_dir == DIR_W:
                    if map[(x-1,y-1)] == '.'and map[(x-1,y)] == '.' and map[(x-1,y+1)] == '.':
                        cdest = (x-1, y)
                        break
                elif consider_dir == DIR_E:
                    if map[(x+1,y-1)] == '.'and map[(x+1,y)] == '.' and map[(x+1,y+1)] == '.':
                        cdest = (x+1, y)
                        break
                consider_dir = nextdir(consider_dir)
            if cdest != None:
                if cdest not in consider:
                    consider[cdest] = (x,y)
                else:
                    consider[cdest] = None

    moved = False
    for ck in consider.keys():
        if consider[ck] != None:
            moved = True
            srcx, srcy = consider[ck]
            dstx, dsty = ck
            assert(map[(dstx, dsty)] == '.')
            map[(dstx, dsty)] = '#'
            assert(map[(srcx, srcy)] == '#')
            map[(srcx, srcy)] = '.'
    return moved

def def_value():
    return '.'

def run():
    lines = open(sys.argv[1]).read().splitlines()
    map = defaultdict(def_value)
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            map[(x,y)] = lines[y][x]

    considerdir = DIR_N
    roundnr = 1
    while True:
        if not round(map, considerdir):
            break
        # printm(map)
        considerdir = nextdir(considerdir)
        if roundnr == 10:
            tl, br = get_bounds(map, lambda map, coord: map[coord] == '#')
            count = 0
            for y in range(tl[1], br[1]+1):
                for x in range(tl[0], br[0]+1):
                    if map[(x,y)] =='.':  
                        count+=1
            print("Part1", count)
                
        roundnr+=1
    print("Part2", roundnr)
run()

