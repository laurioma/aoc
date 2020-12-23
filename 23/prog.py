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

DATALEN1 = 10
MOVES1 = 100
DATALEN2 = 1000000
MOVES2 = 10000000
MAXPRINT = 100

def crab_move(datain, idx):
    removed = []
    newdata = []
    curr = datain[idx]
    if idx < (len(datain) - 3):
        removed = datain[idx+1:idx+4]
        newdata = datain[0:idx+1] + datain[idx+4:]
    else:
        start = 4 - (len(datain) - idx)
        removed = datain[idx+1:] + datain[0:start]
        newdata = datain[start:idx+1] + datain[idx+4:]
    vprint("p", idx, "curr", curr, datain, "newdata",newdata, "removed", removed)

    dstval = datain[idx]
    while True:
        vprint("DST1_", dstval, datain[idx])
        dstval -= 1
        if dstval < 0:
            dstval = len(datain)
        if dstval in newdata and dstval != datain[idx]:
            break
    vprint("DST1", dstval)
    assert(newdata.count(dstval))
    dst = newdata.index(dstval)
    dsti = dst + 1

    for i in (2, 1, 0):
        newdata.insert(dsti, removed[i])
    vprint("curr["+str(idx)+"]="+str(curr), "move v"+ str(dstval)+ "("+ str(dsti)+")", removed, newdata[0:MAXPRINT])

    curp = newdata.index(curr)
    curp += 1
    if curp >= len(datain):
        curp = 0
    return (newdata, curp, dsti)

def part1():
    datain = [7,3,9,8,6,2,5,4,1]
 #   datain = [3,8,9,1,2,5,4,6,7]

    data = datain
    curp = 0
    for i in range(MOVES1):
#        print(curp, "d", data)
        data, curp, _ = crab_move(data, curp)

    print(curp, "F", data)
    start = data.index(1)
    print("Answer1 ", end='')
    for i in range(len(data)):
        start+=1
        if start >= len(data):
            start=0
        print(data[start], end='')
    print()


def printr(ring, start, name=''):
    ptr = start
    print ("Ring",name, end=' ')
    for i in range(len(ring)):
        print (ptr, end=' ')
        ptr = ring[ptr]
    print()

def crab_move2(ring, idx):
    removed = []
    remove = idx
    maxval = len(ring) - 1
    for i in range(3):
        remove = ring[remove]
        vprint("removed", remove)
        removed.append(remove)
    vprint("rem", removed)

    ring[idx] = ring[removed[2]]

    dstval = idx
    while True:
        vprint("DST2_", dstval, ring[idx], maxval, dstval in removed, dstval == idx)
        dstval -= 1
        if dstval < 1:
            dstval = maxval
        if dstval not in removed and dstval != idx:
            break

    vprint ("dstval", dstval, ring[dstval])

    tmp = ring[dstval]
    vprint ("tmp", tmp)
    ring[dstval] = removed[0]
    ring[removed[2]] = tmp

#    printr(ring, idx)

    vprint("ret", ring[idx])
    return ring[idx]


def part2():
    datain = [7,3,9,8,6,2,5,4,1]
    datain = [3,8,9,1,2,5,4,6,7]

    ring = [0]*(DATALEN2+1)
    print(len(ring))
    for i in range(DATALEN2):
        if i < len(datain) - 1:
            ring[datain[i]] = datain[i + 1]
        elif i == len(datain) - 1 :
            ring[datain[-1]] = (i + 2)
        else : 
            ring[i + 1] = (i + 2)
    ring[DATALEN2] = datain[0]

#    print(ring)
#    printr(ring, datain[0])

    idx = datain[0]
    for i in range(MOVES2):
#        printr(ring, idx, "move"+str(i+1))
        idx = crab_move2(ring, idx)

#    printr(ring, idx, "Final"+str(i+1))
    print("Final", ring[1], ring[ring[1]])
    print ("Answer2", ring[1] * ring[ring[1]])
    return


def execute(partnr):
    if partnr == 0:
        part1()
    else:
        part2()

p2 = 0 if len(sys.argv) < 2 else int(sys.argv[1])

execute(p2)