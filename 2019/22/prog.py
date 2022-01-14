import sys
import time
import copy
import re
import itertools
import math
from collections import defaultdict
import matplotlib.pyplot as plt

def dealnew(sz, idx):
    return sz - 1 - idx

def dealcut(sz, idx, pos):
    return (idx - pos) % sz

def dealinc(sz, idx, inc):
    if inc == 0 or inc == 1:
        return idx
    assert(sz % inc != 0)

    roundn = int(idx * inc/sz)
    return idx * inc - (sz*roundn) 

def dealnew_r(sz, idx):
    return sz - 1 - idx

def dealcut_r(sz, idx, pos):
    return (idx + pos) % sz

# inverse of dealinc. n can be found by some tinkering with dealinc
def dealinc_r_eq(sz, idx, inc, n):
    return int(idx / inc )+ n * int(sz / inc)

def dealinc_r(sz, idx, inc):
    if inc == 0 or idx == 0:
        return idx
    assert(sz % inc != 0)
    n = 0
    mod = idx % inc
    modch = mod
    ret = dealinc_r_eq(sz, idx, inc, 0)
    if mod != 0:
        for i in range(inc):
            szch = sz - (inc - modch)
            modch = szch % inc
            if modch == 0:
                n = i+1
                for j in range(inc):
                    ret = dealinc_r_eq(sz, idx, inc, n) + j
                    ch = dealinc(sz, ret, inc)
                    if ch == idx:
                        break
                break

    return ret

def part1(instr):
    numcards = 10007
    cardp = 2019 # 2558
    for i, c in instr:
        # opos = cardp
        if i == 2:
            cardp = dealinc(numcards, cardp, c)
            # print("incr", c, opos, "->", cardp)
        elif(i == 1):
            cardp = dealcut(numcards, cardp, c)
            # print("cut", c, opos, "->", cardp)
        elif i == 0:
            cardp = dealnew(numcards, cardp)
            # print("new", opos, "->", cardp)
        else:
            assert(False), "wrong instr %s" % i

    print("Part1", cardp)

# takes loong time
def part2(instr):
    numcards = 119315717514047
    cardp = 2020 
    times=101741582076661
    for r in range(times):
        for i, c in reversed(instr):
            if i == 2:
                cardp = dealinc_r(numcards, cardp, c)
    #            print("incr", c, opos, "->", cardp)
            elif(i == 1):
                cardp = dealcut_r(numcards, cardp, c)
    #            print("cut", c, opos, "->", cardp)
            elif i == 0:
                cardp = dealnew_r(numcards, cardp)
    #            print("new", opos, "->", cardp)
            else:
                assert(False), "wrong instr %s" % i

    print("Part2", cardp)

# should take less time but still too long
def part21(instr):
    numcards = 119315717514047
    cardp = 2020
    # The positions start from beginning after numcards rounds so we can run forward from this point to numcards
    times = 119315717514047 - 101741582076661 
    for r in range(times):
        for i, c in instr:
            if i == 2:
                cardp = dealinc(numcards, cardp, c)
            elif(i == 1):
                cardp = dealcut(numcards, cardp, c)
            elif i == 0:
                cardp = dealnew(numcards, cardp)
            else:
                assert(False), "wrong instr %s" % i

    print("Part2", cardp)

def run(file):
    data = ""
    with open(file) as f:
        data = f.read()

    rows = data.split('\n')

    instr = []
    for l in rows:
        m = re.search("deal with increment (-?\d+)", l)
        if m:
            inc = int(m.group(1))
            instr.append([2, inc])
        else:
            m = re.search("cut (-?\d+)", l)
            if m:
                c = int(m.group(1))
                instr.append([1, c])
            else:
                m = re.search("deal into new stack", l)
                if m:
                    instr.append([0, 0])
                else:
                    assert(False), "wrong line %s" % l

    part1(instr)
    # part2(instr)
    # part21(instr)
    print ("Part2", '?')

f = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
run(f)