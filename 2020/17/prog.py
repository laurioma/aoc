import sys
import time
import re
import copy

def count_active_neighbours(cube, x, y, z, w):
    size = len(cube)
    counta = 0

    for ww in range(w-1, w+2):
        for zz in range(z-1, z+2):
            for yy in range(y-1, y+2):
                for xx in range(x-1, x+2):
                    if ww >= 0 and ww < size and zz >= 0 and zz < size and yy >= 0 and yy < size and xx >= 0 and xx < size:
                        if ww == w and zz == z and yy == y and xx == x:
                            continue
                        if cube[ww][zz][yy][xx] == "#":
                            counta += 1

    return counta

def count_active(cube):
    size = len(cube)
    counta = 0

    for ww in range(size):
        for zz in range(size):
            for yy in range(size):
                for xx in range(size):
                    if cube[ww][zz][yy][xx] == "#":
                        counta += 1

    return counta


def new_cube(size):
    newnc = []
    for ww in range(size):
        newc = []
        for z in range(size):
            newm = []
            for y in range(size):
                newr = []
                for x in range(size):
                    newr.append(".")
                newm.append(newr)
            newc.append(newm)
        newnc.append(newc)
    return newnc

def copy_expand_cube(cube):
    newnc = []
    size = len(cube)
    for w in range(size+2):
        newc = []
        for z in range(size+2):
            newm = []
            for y in range(size+2):
                newr = []
                for x in range(size+2):
                    if x == 0 or x == size+1 or y == 0 or y == size+1 or z == 0 or z == size+1 or w == 0 or w == size+1:
                        newr.append(".")
                    else:
                        newr.append(cube[w-1][z-1][y-1][x-1])
                newm.append(newr)
            newc.append(newm)
        newnc.append(newc)
    return newnc

def next_cycle(cube):
    ret = copy.deepcopy(cube)
    size = len(cube)
    for w in range(size):
        for z in range(size):
            for y in range(size):
                for x in range(size):
                    c = count_active_neighbours(cube, x, y, z, w)
                    if cube[w][z][y][x] == '#':
                        if c == 2 or c == 3:
                            ret[w][z][y][x] = "#"
                        else:
                            ret[w][z][y][x] = "."
                    else:
                        if c == 3:
                            ret[w][z][y][x] = "#"
                        else:
                            ret[w][z][y][x] = "."
    return ret

def printc(name, cube):
    print("cube", name)
    size = len(cube)
    for w in range(size):
        for z in range(size):
            for y in range(size):
                s = ""
                for x in range(size):
                    s+=cube[w][z][y][x]
                print(s)
            print("")

def execute(file, part2):
    ncube = None
    y = 0
    with open(file) as f:
        for line in f:
            llen = len(line.rstrip())
            if not ncube:
                ncube = new_cube(llen)
            for x in range(llen):
                ncube[1][1][y][x] = line[x]
                print(y, x)
            y+=1
    

    printc("ncube", ncube)
    for i in range(6):
        c1 = copy_expand_cube(ncube)
        ncube = next_cycle(c1)
        printc("cycle"+str(i), ncube)

    print ("Result1", count_active(ncube))

execute(sys.argv[1], int(sys.argv[2]))