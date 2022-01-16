import sys
import time
import copy
import re
import itertools
import math
from collections import defaultdict
import matplotlib.pyplot as plt


NEW = 0
CUT = 1
INC = 2

def dealnew(sz, idx):
    return (-idx - 1) % sz
def dealinc(sz, idx, inc):
    return ( idx * inc) % sz
def dealcut(sz, idx, pos):
    return ( idx - pos) % sz

def part1(instr):
    numcards = 10007
    cardp = 2019
    for i, c in instr:
        opos = cardp
        if i == INC:
            cardp = dealinc(numcards, cardp, c)
            # print("incr", c, opos, "->", cardp)
        elif i == CUT:
            cardp = dealcut(numcards, cardp, c)
            # print("cut", c, opos, "->", cardp)
        elif i == NEW:
            cardp = dealnew(numcards, cardp)
            # print("new", opos, "->", cardp)
        else:
            assert(False), "wrong instr %s" % i

    print("Part1", cardp)


def part2(instr):
    numcards = 119315717514047
    cardp = 2020
    A=1
    B=0
    # dealnew, dealicut & dealinc can all be represented as y = A*x+B polynomials. So we combine them into one this way y = A1*(A0*x+B0) + B1
    # can do also %numcards for both A and B on each step to avoid getting too large numbers (A*x mod N + B mod N = (A*x+B) mod N)
    for i, c in instr:
        if i == INC:
            B=(c*B+0)%numcards
            A=(A*c)%numcards
            # print("incr", c, A, B, (cardp * A + B) % numcards)
        elif i == CUT:
            B=(1*B-c)%numcards
            A=(A*1)%numcards
            # print("cut", c, A, B, (cardp * A + B) % numcards)
        elif i == NEW:
            B=(-1*B-1)%numcards
            A=(A*-1)%numcards
            # print("new", A, B, (cardp * A + B) % numcards)
        else:
            assert(False), "wrong instr %s" % i

    numshuffle = 101741582076661
    # as experimentation shows that numbers start repeating after numcards-1 shufflings.
    # Therefore instead of calculating backwards from the 2020 to the start we can take the card position 2020
    # and do numcards - 1 - numshuffle more shufflings to get same "factory order" cards as we had at the beginning.
    # Card number there will be the answer
    numshuffle = numcards - 1 - numshuffle

    # combine multiple polynomials y = Ax*B => yn = A^N*x + B*(A^N-1 + A^N-2 .. + A + 1)
    # For the last part use https://www.wolframalpha.com/input/?i=sum+x%5Ek%2C+k%3D0+to+n&lk=3
    # and get yn = A^N*x + B*(A^N - 1)/(A-1)
    # now A^N*x is easy since we can just as well use modular exponent A^N*x mod N
    A1 = pow(A, numshuffle, numcards)
    # B*(A^N - 1)/(A-1) is more complicated: https://www.quora.com/Is-there-a-fast-way-to-compute-the-sum-of-a-geometric-series-modulo-a-given-integer-i-e-1-a-a-2-ldots-a-n-mod-m-where-a-m-and-n-are-integers
    # so apparently modular exponent can be used for A^N 
    # 1/A-1 mod N == (A-1)^(N-2) mod N according to https://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Using_Euler's_theorem
    # so we get B*(A^N - 1) * (A-1)^(N-2)
    B1 = B * (pow(A, numshuffle, numcards) - 1) * pow(A - 1, numcards-2, numcards)

    print("Part2", (cardp * A1 + B1) % numcards)

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
    part2(instr)

f = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
run(f)