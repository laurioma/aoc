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

# avoid adding duplicates
def add_if_not_there(q, qset, pos, round):
    if not (pos, round) in qset:    
        qset.add((pos, round))
        q.append((pos, round))

def bfs(blz,w,h, start, end):
    blzrounds = {}
    qset = set()
    q = [(start, 0)]
    qset.add((start,0))
    blzrounds[0] = blz
    while q:
        (coord, round) = q.pop(0)
        qset.remove((coord, round))
        blz = blzrounds[round]

        if coord == end:
            return round, blz

        nround = round + 1

        if nround not in blzrounds:            
            blz = step(blz,w,h)
            blzrounds[nround] = blz
        else:
            blz = blzrounds[nround]

        #stay in place
        if len(blz[coord]) == 0:
            add_if_not_there(q, qset, coord, nround)

        #move UDLW
        dirs = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        for d in dirs:
            x = coord[0] + d[0]
            y = coord[1] + d[1]

            if (1 <= x <= w-2 and 1 <= y <= h-2 or (x,y)==end) and len(blz[(x,y)]) == 0:
                add_if_not_there(q, qset, (x, y), nround)
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

