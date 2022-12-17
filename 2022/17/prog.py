import sys
import copy

def get_bounds(matrix):
    ymin = xmin = sys.maxsize
    xmax = ymax = -sys.maxsize
    for (x,y) in matrix.keys():
        xmin = min(xmin, x)
        xmax = max(xmax, x)
        ymin = min(ymin, y)
        ymax = max(ymax, y)
    tl = (xmin, ymin)
    br = (xmax, ymax)
    return (tl, br)

def printm(img):
    tl, br = get_bounds(img)
    tl = (LWALL, tl[1])
    br = (RWALL, br[1])
    for y in range(tl[1], br[1]+1):
        for x in range(tl[0], br[0]+1):
            print(img[(x,y)] if (x, y) in img else '.', end='')
        print("")
    print(tl, br)

def printshapes(shapes):
    room = {}
    for shape in shapes:
        for c in shape[0]:
            room[(c[0],c[1])] = '#'
    printm(room)

shapes = [
    [[0,0], [1,0], [2,0], [3,0]],           #-
    [[1,0], [0,1], [1,1], [2,1], [1,2]],    #+
    [[2,0], [2,1], [2,2], [1,2], [0,2]],    #_|
    [[0,0], [0,1], [0,2], [0,3]],           #|
    [[0,0], [1,0], [0,1], [1,1]]            ##
]

DIRL = "<"
DIRR = ">"
DIRD = "D"
DIRU = "U"

FLOORY = 0
LWALL = 0
RWALL = 6

def opposite(cmd):
    if cmd == DIRL:
        return DIRR
    if cmd == DIRR:
        return DIRL
    if cmd == DIRD:
        return DIRU
    if cmd == DIRU:
        return DIRD
    assert(False)

def move_(shape, dir, steps):
    for s in shape:
        if dir == DIRL:
            s[0]-=steps
        elif dir == DIRR:
            s[0]+=steps
        elif dir == DIRU:
            s[1]-=steps
        elif dir == DIRD:
            s[1]+=steps

def move(shape, shapes, dir, steps):
    didmove = True
    move_(shape,dir,steps)
    if collides(shape, shapes):
        rdir = opposite(dir)
        move_(shape,rdir,steps)
        didmove = False
    return didmove

def collides(shape, shapes):
    for c in shape:
        if c[0] == (LWALL - 1):
            return True

    for c in shape:
        if c[0] == (RWALL + 1):
            return True

    for c in shape:
        if c[1] == FLOORY:
            return True

    for c in shape:
        for rs in shapes:
            for rc in rs[0]:
                if c == rc:
                    return True
    return False

def height(shape):
    maxy = -sys.maxsize
    miny = sys.maxsize
    for c in shape:
        if maxy < c[1]:
            maxy = c[1]
        if miny > c[1]:
            miny = c[1]
    return (maxy - miny)+1

def get_highest(shapes):
    maxy = sys.maxsize
    for shape in shapes:
        for c in shape[0]:
            if maxy > c[1]:
                maxy = c[1]
    return maxy

def prune_shapes(shapes, minheight):
    ret = []
    for rs in shapes:
        if rs[0][0][1] < -minheight:
            ret.append(rs)
    return ret

def stepsim(roomshapes, si, cmdi, cmds, highest):
    shape=shapes[si]
    fshape = copy.deepcopy(shape)
    assert(move(fshape, [], DIRU, highest + 3 + height(fshape)))
    assert(move(fshape, [], DIRR, 2)) # move 2 units right from wall
    relpos = [0,0]
    while True:
        assert(not collides(fshape, roomshapes))
        if cmdi >= len(cmds):
            cmdi = 0
        cmd = cmds[cmdi]
        cmdi+=1

        if move(fshape, roomshapes, cmd, 1):
            relpos[0] += -1 if cmd == DIRL else 1

        assert(not collides(fshape, roomshapes))
        if not move(fshape, roomshapes, DIRD, 1):
            break
        else:
            relpos[1]+=1

    roomshapes.append([fshape, si, relpos])
    # printshapes(roomshapes)
    highest = abs(get_highest(roomshapes))
    roomshapes = prune_shapes(roomshapes, highest - 100)
    return (roomshapes, cmdi, highest)


def part1():
    cmds = open(sys.argv[1]).read()
    highest = 0
    roomshapes = []
    cmdi = 0
    rockcnt = 0
    maxiter = 2022
    while rockcnt < maxiter:
        for si in range(len(shapes)):
            (roomshapes, cmdi, highest) = stepsim(roomshapes, si, cmdi, cmds, highest)
            rockcnt += 1
            
            if rockcnt == maxiter:
                break
    print("Part1: ", highest)


def get_cachei(si, cmdi, roomshapes, maxlast):
    lastshapes = ""
    for i in range(len(roomshapes)-1, len(roomshapes)-maxlast, -1):
        if i < 0:
            break
        lastshapes += str(roomshapes[i][1]) + str(roomshapes[i][2][0]) + str(roomshapes[i][2][1])
    return (si, cmdi, lastshapes)


def part2():
    cmds = open(sys.argv[1]).read()
    highest = 0
    roomshapes = []
    cmdi = 0
    rockcnt = 0

    cache = {}
    desired = 1000000000000
    period = 0
    period_start = 0
    period_height = 0
    while True:
        for si in range(len(shapes)):
            cachei = get_cachei(si, cmdi, roomshapes, 20)
            if cachei in cache:
                (prevcnt, prevhighest) =  cache[cachei]
                period = rockcnt - prevcnt
                period_start = prevcnt
                period_height = highest - prevhighest
                break

            cache[cachei] = (rockcnt, highest)
            (roomshapes, cmdi, highest) = stepsim(roomshapes, si, cmdi, cmds, highest)

            rockcnt += 1
        if period > 0:
            break 

    rockcnt = 0
    remaining = (desired - period_start) % period
    runcnt = remaining + period_start
    highest = 0
    roomshapes = []
    cmdi = 0
    while rockcnt < runcnt:
        for si in range(len(shapes)):
            (roomshapes, cmdi, highest) = stepsim(roomshapes, si, cmdi, cmds, highest)
            rockcnt += 1
            if rockcnt == runcnt:
                break

    print("Part2: ", int((desired - period_start)/period) * period_height + highest)

part1()
part2()
