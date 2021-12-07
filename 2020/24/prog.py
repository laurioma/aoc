import sys
import time
import copy
import re
import itertools
import profile


def vprint(*args, end='\n'):
    verb = 0
    if verb:
        print(*args, end=end)

def move(coord, c):
    if c == "ne":
        if coord[1] % 2 != 0:
            return (coord[0] + 1, coord[1] - 1)
        else:
            return (coord[0], coord[1] - 1)
    elif c == "sw":
        if coord[1] % 2 != 1:
            return (coord[0] - 1, coord[1] + 1)
        else:
            return (coord[0], coord[1] + 1)
    elif c == "nw":
        if coord[1] % 2 == 0:
            return (coord[0] - 1, coord[1] - 1)
        else:
            return (coord[0], coord[1] - 1)
    elif c == "se":
        if coord[1] % 2 != 0:
            return (coord[0] + 1, coord[1] + 1)
        else:
            return (coord[0], coord[1] + 1)
    elif c == "e":
        return (coord[0] + 1, coord[1])
    else:
        return (coord[0] - 1, coord[1])

coordscache = {}

def get_neighbours(coord):
    global coordscache
    if coord in coordscache:
        return coordscache[coord]
    ncoords = []
    for c in ("ne", "sw", "nw", "se", "e", "w"):
        ncoords.append(move(coord, c))
    coordscache[coord] = ncoords
    return ncoords

def count_neighbours(flipped, tile):
    count = 0
    for n in get_neighbours(tile):
        if n in flipped:
            count +=1
    return count

NUMDAYS = 100

def printt(flipped):
    minx = miny = -1
    maxx = maxy = 1
    if len(flipped):
        maxx = max(flipped, key=lambda x: x[0])[0]
        minx = min(flipped, key=lambda x: x[0])[0]
        maxy = max(flipped, key=lambda x: x[1])[1]
        miny = min(flipped, key=lambda x: x[1])[1]
    print("   ", end='')
    for x in range(minx, maxx+1):
        print ("{0:2}".format(x),end='')
    print()
    for y in range(miny, maxy+1):
        print("{0:2} ".format(y), end='')
        if y % 2 == 1:
            print(" ", end = '')
        for x in range(minx, maxx+1):
            if (x, y) in flipped:
                print ("B", end=" ")
            else:
                print ("W", end=" ")
        print()

def part2(flipped):
#    printt(flipped)
    for i in range(NUMDAYS):
        new = set()
        # copy blacks
        for f in flipped:
            cn = count_neighbours(flipped, f)
            if cn == 0 or cn > 2:
                pass
            else:
                new.add(f)
        
            # go over all the whites
            neighbours = get_neighbours(f)
#            print("ne", len(neighbours))
            for n in neighbours:
                if count_neighbours(flipped, n) == 2 and n not in flipped:
                    new.add(n)
        print("day", i+1, len(new))
        flipped = new
#        printt(flipped)

    print ("Answer2", len(new))


def execute(file, partnr):
    with open(file) as f:
        data = f.read()

    rows = data.split('\n')

    patterns = ["e", "se", "sw", "w," "nw", "ne"]

    linecmds = []
    for line in rows:
        cmd = []
        idx = 0
        while idx < len(line):
            if idx < len(line) - 1 and line[idx:idx+2] == "se":
                cmd.append("se")
                idx += 2
            elif idx < len(line) - 1 and line[idx:idx+2] == "sw":
                cmd.append("sw")
                idx += 2
            elif idx < len(line) - 1 and line[idx:idx+2] == "nw":
                cmd.append("nw")
                idx += 2
            elif idx < len(line) - 1 and line[idx:idx+2] == "ne":
                cmd.append("ne")
                idx += 2
            elif idx < len(line) and line[idx] == "e":
                cmd.append("e")
                idx += 1
            else:
                assert(line[idx] == "w"), line[idx]
                cmd.append("w")
                idx += 1
        linecmds.append(cmd)

#    print(linecmds)

    flipped = set()
    for lc in linecmds:
        offsc = (0,0) # x, y
        for c in lc:
            b4 = offsc
            offsc = move(offsc, c)
#            print ("cmd", c, b4, "->", offsc)

        if offsc in flipped:
            flipped.remove(offsc)
        else:
            flipped.add(offsc)
#        print(offsc)
    print ("Answer1", len(flipped))

    part2(flipped)

#    if partnr == 0:
#        part1()
#    else:
#        part2()

f = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
p2 = "input.txt" if len(sys.argv) < 3 else int(sys.argv[2])

execute(f, p2)