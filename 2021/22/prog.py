import sys
import itertools
import re
from collections import defaultdict

def range2(start, stop, bounds):
    step = 1
    if bounds[0] and bounds[0] > start:
        start = bounds[0] 
    if bounds[1] and bounds[1] < stop:
        stop = bounds[0]
    return range(start, stop + step, step)

def part1(instr):
    cuboids = {}
    bounds = (-50,50)
    for i in instr:
        c = i[1]
        if i[0] == "on":
            for x, y, z in itertools.product(range2(c[0][0], c[0][1], bounds), range2(c[1][0], c[1][1], bounds), range2(c[2][0], c[2][1], bounds)):
                cuboids[(x, y, z)] = 1
        elif i[0] == "off":
            for x, y, z in itertools.product(range2(c[0][0], c[0][1], bounds), range2(c[1][0], c[1][1], bounds), range2(c[2][0], c[2][1], bounds)):
                if (x, y, z) in cuboids:
                    del cuboids[(x, y, z)]
    print("Part1", len(cuboids))

def count(i):
    if i[0][0] == i[0][1] == -1 or  i[1][0] == i[1][1] == -1 or i[2][0] == i[2][1] == -1:
        return 0
    return (i[0][1] - i[0][0] + 1) * (i[1][1] - i[1][0]+1) * (i[2][1] - i[2][0]+1)

def isbetween(a,b,c):
    if a <= c and b >= c:
        return True
    return False

def range_overlap(a,b):
    overlap = (-1,-1)
    if isbetween(a[0], a[1], b[0]):
        if isbetween(a[0], a[1], b[1]):
            overlap = (b[0], b[1])
        else:
            overlap = (b[0], a[1])
    elif isbetween(b[0], b[1], a[0]):
        if isbetween(b[0], b[1], a[1]):
            overlap = (a[0], a[1])
        else:
            overlap = (a[0], b[1])

    return overlap

def is_inside(a, b):
    return a[0][0] >= b[0][0] and a[0][1] <= b[0][1] and a[1][0] >= b[1][0] and a[1][1] <= b[1][1] and a[2][0] >= b[2][0] and a[2][1] <= b[2][1]

def overlap(a, b):
    xol = range_overlap(a[0], b[0])
    if xol == (-1, -1):
        return (xol, xol, xol)
    yol = range_overlap(a[1], b[1])
    if yol == (-1, -1):
        return (yol, yol, yol)
    zol = range_overlap(a[2], b[2])
    if zol == (-1, -1):
        return (zol, zol, zol)
    return (xol, yol, zol)

def is_overlapping(a, b):
    return overlap(a, b) != ((-1, -1), (-1, -1), (-1, -1)) 

def range_outside(a, b):
    o = []
    if isbetween(a[0], a[1], b[0]):
        if a[0] <= b[0]-1:
            o.append((a[0], b[0]-1))
    if isbetween(a[0], a[1], b[1]):
        if b[1]+1 <= a[1]:
            o.append((b[1]+1, a[1]))
    return o

# break up a if it's overlapping with b, return list of cubes matching size of a-b
def get_non_overlapping(a, b):
    assert(count(overlap(a, b)) != 0)
    ret = []
    xol = range_overlap(a[0], b[0])
    yol = range_overlap(a[1], b[1])
    zol = range_overlap(a[2], b[2])           
    xout = range_outside(a[0], b[0])
    yout = range_outside(a[1], b[1])
    zout = range_outside(a[2], b[2])
    
    assert(xol != (-1,-1))
    assert(yol != (-1,-1))
    assert(zol != (-1,-1))
    # add up to 2 cubes with outside x and original y and z dimensions
    for xo in xout:
        ret.append((xo, a[1], a[2]))
    # add up to 2 cubes with overlapping x, outside y and original z dimensions
    for yo in yout:
        ret.append((xol, yo, a[2]))
    # add up to 2 cubes with overlapping x, overlapping y and outside z dimensions
    for zo in zout:
        ret.append((xol, yol, zo))

    return ret

def part2(instr):
    added = []
    for i in instr:
        # while there is overlapping cubes, break them up
        if len(added) == 0:
            added.append(i[1])
        else:
            remove = []
            add = []
            for a in range(len(added)):
                if is_overlapping(added[a], i[1]):
                    remove.append(a)
                    nol = get_non_overlapping(added[a], i[1])
                    for n in nol:
                        add.append(n)
            # if its on block then add block itself as well
            if i[0] == "on":
                add.append(i[1])
            remove.sort(reverse=True)
            for r in remove:
                added.pop(r)
            for a in add:
                added.append(a)
        # for a,b in itertools.combinations(range(len(added)),2):
        #      if is_overlapping(added[a], added[b]):
        #          print("OVERLAP!", added[a], added[b])
        #          assert False

    sum = 0
    for a in added:
        sum += count(a)
    print("Part2", sum)

def run():
    lines = open(sys.argv[1]).read().splitlines()
    instr = []
    for l in lines:
        m = re.search('([^\s-]+) x=([0-9-]+)..([0-9-]+),y=([0-9-]+)..([0-9-]+),z=([0-9-]+)..([0-9-]+)', l)
        assert(m)
        x = (int(m.group(2)), int(m.group(3)))
        y = (int(m.group(4)), int(m.group(5)))
        z = (int(m.group(6)), int(m.group(7)))
        if x[0] > x[1]:
            print("x", x)
        if y[0] > y[1]:
            print("y", y)
        if z[0] > z[1]:
            print("z", z)
        t = (m.group(1), (x, y, z))
        instr.append(t)

    part1(instr)
    part2(instr)

run()
