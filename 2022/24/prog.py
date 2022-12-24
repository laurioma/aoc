import sys
from collections import defaultdict
import itertools

BLZ_UP = '^'
BLZ_DOWN = 'v'
BLZ_LEFT='<'
BLZ_RIGHT='>'
BLIZZARDS = [BLZ_UP, BLZ_DOWN, BLZ_LEFT, BLZ_RIGHT]

def printm(blz, s, e, pos, w, h):
    for y in range(h):
        for x in range(w):
            if x == 0 or x == w-1 or y == 0 or y == h-1:
                if (x,y) == pos:
                    print('E', end='')
                elif (x,y) == s or (x,y) == e:
                    print('.', end='')
                else:    
                    print('#', end='')
            else:
                b = blz[(x,y)]
                if len(b) == 1:
                    print(b[0], end='')
                elif len(b) > 1:
                    print(len(b), end='')
                elif (x,y) == pos:
                    print('E', end='')
                else:
                    print('.', end='')
        print("")

def step(blz, w,h):
    blzn = defaultdict(lambda: []) 
    for x,y in blz.keys():
        for dir in blz[(x,y)]:
            xn = x
            yn = y
            if dir == BLZ_UP:
                yn = y-1
                if yn == 0:
                    yn = h-2
            elif dir == BLZ_DOWN:
                yn = y+1
                if yn == h-1:
                    yn = 1
            elif dir == BLZ_LEFT:
                xn = x-1
                if xn == 0:
                    xn = w-2
            elif dir == BLZ_RIGHT:
                xn = x+1
                if xn == w-1:
                    xn = 1
            blzn[(xn,yn)].append(dir)
    return blzn

def get_blizzards(matrix, w, h):
    blizzards = defaultdict(lambda: [])
    for y, x in itertools.product(range(h), range(w)):
        if matrix[y][x] in BLIZZARDS:
            blizzards[(x,y)].append(matrix[y][x])
    return blizzards

def bfs(blz,w,h, start, end):
    scoords=set([start])
    for round in range(10000):
        nscoords=set()
        for coord in scoords:
            #stay in place
            if len(blz[coord]) == 0:
                nscoords.add(coord)

            #move UDLW
            dirs = [(-1, 0), (0, -1), (0, 1), (1, 0)]
            for d in dirs:
                x = coord[0] + d[0]
                y = coord[1] + d[1]
                if (x,y) == end:
                    return round, blz
                if 1 <= x <= w-2 and 1 <= y <= h-2 and len(blz[(x,y)]) == 0:
                    nscoords.add((x,y))
        blz = step(blz,w,h)
        scoords = nscoords

    return -1, {}

def run():
    lines = open(sys.argv[1]).read().splitlines()
    matrix = [list(row) for row in lines]; w=len(matrix[0]); h=len(matrix)

    blz = get_blizzards(matrix, w, h)
    start = (1,0)
    end = (w-2,h-1)

    # printm(blz, start, end, pos,w,h)
    rounds, blz = bfs(blz, w,h, start, end)
    assert(rounds > 0)
    print("Part1", rounds)
    rounds2, blz = bfs(blz, w,h, end, start)
    assert(rounds2 > 0)
    rounds3, blz = bfs(blz, w,h, start, end)
    assert(rounds3 > 0)
    print("Part2", rounds+rounds2+rounds3)

run()

