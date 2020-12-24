import sys
import time
import copy
import re
import itertools
import profile
from collections import defaultdict


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
    for f in flipped:
        if f in get_neighbours(tile):
            count +=1
    return count

NUMDAYS = 100

def part2(flipped):
    for i in range(NUMDAYS):
        new = defaultdict(lambda: (0))
        # copy blacks
        for f in flipped:
            cn = count_neighbours(flipped, f)
            if cn == 0 or cn >= 2:
                pass
            else:
                new[f] = 1
        
            # go over all the whites
            neighbours = get_neighbours(f)
#            print("ne", len(neighbours))
            for n in neighbours:
                if n not in new.keys() and count_neighbours(flipped, n) == 2: #and n not in flipped.keys(): #why?
                    new[n] = 1
        print("day", i+1, len(new))
        flipped = new
    
    count = 0
    for t in new:
        count +=1
    print ("Answer2", count)


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

    print(linecmds)

    flipped = defaultdict(lambda: (0))
    for lc in linecmds:
        offsc = (0,0) # x, y
        for c in lc:
            b4 = offsc
            offsc = move(offsc, c)
            print ("cmd", c, b4, "->", offsc)

        if offsc in flipped:
            del flipped[offsc]
        else:
            flipped[offsc] = 1
        print(offsc)
    print(len(flipped))

    count = 0
    for t in flipped:
        count +=1
    print ("Answer1", count)

    part2(flipped)

#    if partnr == 0:
#        part1()
#    else:
#        part2()

f = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
p2 = "input.txt" if len(sys.argv) < 3 else int(sys.argv[2])

execute(f, p2)