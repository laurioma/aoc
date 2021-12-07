import sys
import time
import copy
import re
import itertools
from collections import defaultdict

def dealnew(cards):
    return list(reversed(cards))


def dealcut(cards, pos):
    return cards[pos:] + cards[0:pos]

def dealinc(cards, inc):
    ret = [-1]* len(cards)
    idx = 0
    left = 0
    for i in range(len(cards)):
        assert (ret[idx] == -1), ret[idx]
        ret[idx] = cards[i]
        idx = (idx + inc) % len(cards)
        if idx == left:
            idx += 1
            left = idx

    assert(ret.count(-1) == 0), ret
    return ret

def dealnew1(sz, idx):
    return sz - 1 - idx

def dealcut1(sz, idx, pos):
    return (idx - pos) % sz

def dealinc1(sz, idx, inc):
    ii = 0
    left = 0
    for i in range(sz):
#        print("inc", inc, "idx", idx, "ii", ii, "left", left, "i", i)
        if i == idx:
            return ii

        ii = (ii + inc) % sz
        if ii == left:
            ii += 1
            left = ii
 
#    print("ii", ii, "left")
    assert()

def dealnew_r(sz, idx):
    return sz - 1 - idx

def dealcut_r(sz, idx, pos):
    return (idx + pos) % sz

def dealinc_r(sz, idx, inc):
    ii = 0
    left = 0
    for i in range(sz):
#        print("REV inc", inc, "idx", idx, "ii", ii, "left", left, "i", i)
        if ii == idx:
            return i

        ii = (ii + inc) % sz
        if ii == left:
            ii += 1
            left = ii
 
#    print("REV", "ii", ii, "left")
    assert()

def dealnew2(cards):
    ret = []
    for i in range(len(cards)):
        ii = dealnew1(len(cards), i)
        ret.append(cards[ii])
    return ret

def dealcut2(cards, pos):
    ret = []
    for i in range(len(cards)):
        ii = dealcut1(len(cards), i, pos)
        ret.append(cards[ii])
    return ret

def dealinc2(cards, inc):
    ret = []
    for i in range(len(cards)):
        ii = dealinc1(len(cards), i, inc)
        ret.append(cards[ii])
    return ret


#NUMCARDS = 119315717514047
NUMCARDS = 10007
#NUMCARDS = 10

def part1(instr):
    cards = [i for i in range(NUMCARDS)]
    print(cards)
    for i, c in instr:
        if i == 2:
            cards = dealinc(cards, c)
            print("incr", c, cards)
        elif(i == 1):
            cards = dealcut(cards, c)
            print("cut", c, cards)
        elif i == 0:
            cards = dealnew(cards)
            print("new",cards)
        else:
            assert(False), "wrong instr %s" % i

    print(cards)
    if NUMCARDS > 10:
        print ("RES", cards.index(2019))

def part11(instr):
    cardp = 2019 # 2558
#    cardp = 8 #3
    for i, c in instr:
        opos = cardp
        if i == 2:
            cardp = dealinc1(NUMCARDS, cardp, c)
            print("incr", c, opos, "->", cardp)
        elif(i == 1):
            cardp = dealcut1(NUMCARDS, cardp, c)
            print("cut", c, opos, "->", cardp)
        elif i == 0:
            cardp = dealnew1(NUMCARDS, cardp)
            print("new", opos, "->", cardp)
        else:
            assert(False), "wrong instr %s" % i

    print("Final pos", cardp)



#def generate(idx, instr):
#    for i,c in reversed(instr):

def part2(instr):
    cardp = 2558 # 2019
#    cardp = 3 #8
#    cardp = 2020
    sol = set()
    for r in range(1000):
        for i, c in reversed(instr):
            opos = cardp
            if i == 2:
                cardp = dealinc_r(NUMCARDS, cardp, c)
    #            print("incr", c, opos, "->", cardp)
            elif(i == 1):
                cardp = dealcut_r(NUMCARDS, cardp, c)
    #            print("cut", c, opos, "->", cardp)
            elif i == 0:
                cardp = dealnew_r(NUMCARDS, cardp)
    #            print("new", opos, "->", cardp)
            else:
                assert(False), "wrong instr %s" % i
        if cardp in sol:
            print("Was!!")
        sol.add(cardp)
        print(r, cardp)

    print("Final pos", cardp)


def test():
    print("test")

    cc = [x for x in range(NUMCARDS)]
    ccc = dealinc(cc, 4)
    print("dealinc 4", cc, "->", ccc)
    for p in range(NUMCARDS):
        for i in range(10):
            print ("test", i, p)
            ii = dealinc1(NUMCARDS, i, p)
            print ("MOVED ", i, ii)
            iii = dealinc_r(NUMCARDS, ii, p)
            print("REMOVED ", ii, iii)
            assert(iii == i)


# find all lines containi
def execute(file, partnr):
    global nump
    data = ""
    with open(file) as f:
        data = f.read()

#    test()
#    return
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
    if partnr == 0:
        part1(instr)
    elif partnr == 1:
        part11(instr)
    else:
        part2(instr)
    
f = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
p2 = 0 if len(sys.argv) < 3 else int(sys.argv[2])
print ("P2", p2)
execute(f, p2)