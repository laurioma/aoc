import sys
import re

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

def printm(img, tl, br):
    for y in range(tl[1], br[1]+1):
        for x in range(tl[0], br[0]+1):
            print(img[(x,y)] if (x, y) in img else '.', end='')
        print("")

def parse_sensors():
    sensors = []
    lines = open(sys.argv[1]).read().splitlines()
    for l in lines:
        m = re.search('Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', l);
        assert(m)
        x = int(m.group(1))
        y = int(m.group(2))
        xb = int(m.group(3))
        yb = int(m.group(4))
        s = (x,y)
        b = (xb,yb)
        d = mdist(s,b)
        sensors.append((s,b,d))
    return sensors

def in_bounds(p, bound):
    return p[0] >= 0 and p[1] >= 0 and p[0] <= bound and p[1] <= bound

def mdist(start, stop):
    return abs(start[0] - stop[0]) +  abs(start[1] - stop[1])


def mline45(start, stop, bound):
    (x,y) = start
    points = []
    # print("line", start, stop)
    while (x,y) != stop:
        if in_bounds((x,y), bound):
            points.append((x,y))
        x = x + (1 if stop[0] > start[0] else -1)
        y = y + (1 if stop[1] > start[1] else -1)

    return points

def mcircle(p, r, bound):
    res = []
    res += mline45((p[0] - r,p[1]),(p[0], p[1] - r), bound)
    res += mline45((p[0] - r,p[1]),(p[0], p[1] + r), bound)
    res += mline45((p[0] + r,p[1]),(p[0], p[1] - r), bound)
    res += mline45((p[0] + r,p[1]),(p[0], p[1] + r), bound)
    return res

def part1():
    chkrow = 10 if sys.argv[1] == "test.txt" else 2000000
    sensors = parse_sensors()
    smap = {}
    for (s, b, d) in sensors:
        smap[s] = 'S'
        smap[b] = 'B'

    for (s, b, d) in sensors:
        for x in range(-d + s[0], d + s[0]+1):
            if mdist(s, (x,chkrow)) <= d:
                if (x,chkrow) not in smap:
                    smap[(x,chkrow)] = '#'
     
    (tl, br) = get_bounds(smap)
    # printm(map, tl, br)
    cnt = 0
    for x in range(tl[0], br[0]+1):
        if (x, chkrow) in smap and smap[(x,chkrow)] != 'B':
            cnt += 1

    print ('Part1', cnt)

def part2():
    bound = 20 if sys.argv[1] == "test.txt" else 4000000
    sensors = parse_sensors()

    for (s,b,d) in sensors:
        c = mcircle(s, d+1, bound)
        for cp in c:
            canbe = True
            for (s1,b1,d1) in sensors:
                if s == s1:
                    continue
                chkd = mdist(s1, cp)
                if chkd <= d1:
                    canbe = False
                    break
            if canbe:
                if in_bounds(cp, bound) :
                    print ('Part2', cp[0]*4000000 + cp[1])
                    return
    print("Part2: didn't find")

part1()
part2()
