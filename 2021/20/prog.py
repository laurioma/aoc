import sys
import itertools
import re
import json
from collections import defaultdict
import numpy as np
import math

MARGIN = 5

def printm(img, tl, br):
    for y in range(tl[1], br[1]+1):
        for x in range(tl[0], br[0]+1):
            print('#' if img[(x, y)] else '.', end='')
        print("")

def countm(img, tl, br):
    count = 0
    for y in range(tl[1], br[1]+1):
        for x in range(tl[0], br[0]+1):
            count += img[(x, y)]
    return count

def calcpix(xy, img, enh):
    binstr = ""
    for y in range(xy[1]-1, xy[1]+2):
        for x in range(xy[0]-1, xy[0]+2): 
            binstr += "1" if img[(x,y)] else "0" 
    idx = int(binstr, 2)
#    print(idx)
    return enh[idx]

def enhance(img, enh, tl, br):
    newimg = defaultdict(int)
    for y in range(tl[1], br[1]):
        for x in range(tl[0], br[0]):
            if calcpix((x, y), img, enh) == '#':
                newimg[(x, y)] = 1
    return newimg

def runsim(img, enh, wh, n):
    tl = (0, 0)
    br = (wh, wh)
    margin = 5
    for n in range(n):
        tl = (tl[0] - margin, tl[1] - margin)
        br = (br[0] + margin, br[1] + margin)
        img = enhance(img, enh, tl, br)
#        printm(img, tl, br)
        if n % 2 == 0:
            tl = (tl[0] + margin + 1, tl[1] + margin + 1)
            br = (br[0] - margin - 1, br[1] - margin - 1)

    return countm(img, tl, br)

def run():
    lines = open(sys.argv[1]).read().splitlines()
    enh = lines[0]
    img = defaultdict(int)
    for y in range(2, len(lines)):
        line = lines[y]
        for x in range(len(line)):
            if line[x] == '#':
                img[(x, y-2)] = 1

    print("Part1",  runsim(img, enh, len(lines) - 2, 2))
    print("Part2",  runsim(img, enh, len(lines) - 2, 50))

run()
