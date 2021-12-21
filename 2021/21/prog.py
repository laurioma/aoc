import sys
import itertools
import re
import math
from collections import defaultdict
import copy

value = 1
def roll():
    global value
    ret = value
    value += 1
    if value > 100:
        value = 1
    return ret

def move(pos, cnt):
    return ((pos+cnt - 1) % 10) + 1

def part1(p1pos, p2pos):
    p1score = 0
    p2score = 0
    rolls = 0
    while True:
        for _ in range(3):
            rolls += 1
            p1r = roll()
            p1new = move(p1pos, p1r)
            p1pos = p1new

        p1score += p1pos
        if p1score >= 1000:
            break

        for _ in range(3):
            rolls += 1
            p2r = roll()
            p2pos = move(p2pos, p2r)

        p2score += p2pos
        if p2score >= 1000:
            break
    print("Part1",  rolls * (p2score if p1score > p2score else p1score))


rollcnt = 0
def roll21():
    global rollcnt
    rollcnt += 1
    # if rollcnt == 1:
    #     return 2
    return 1

def move(pos, cnt):
    return ((pos+cnt - 1) % 10) + 1

def part21(p1pos, p2pos):
    p1score = 0
    p2score = 0
    rolls = 0
    while True:
        p1rs = 0
        for _ in range(3):
            rolls += 1
            p1r = roll21()
            p1new = move(p1pos, p1r)
            p1pos = p1new
            p1rs += p1r

        p1score += p1pos
        if p1score >= 21:
            print("Part21 P1W",  p1rs, p2rs, "pos", p1pos, p2pos, "sc", p1score, p2score)
            break

        p2rs = 0
        for _ in range(3):
            rolls += 1
            p2r = roll21()
            p2pos = move(p2pos, p2r)
            p2rs += p2r

        p2score += p2pos
        if p2score >= 21:
            print("Part21 P2W",  p1rs, p2rs, "pos", p1pos, p2pos, "sc", p1score, p2score)
            break
        print("Part21",  p1rs, p2rs, "pos", p1pos, p2pos, "sc", p1score, p2score)
    
    print("Part21")

def part2_round(l, dicemap, p1pos, p2pos, p1score, p2score, cnt1, cnt2, draws1, draws2):
#    print("level", l, "pos", p1pos, p2pos, "score", p1score, p2score, "cnt",  cnt1, cnt2)
    p1wins = 0
    p2wins = 0
    for p1r in dicemap:
        p1cnt = dicemap[p1r]
#        print("level", l, "p1 draw", p1r, p1cnt)
        p1posnew = move(p1pos, p1r)
        p1scorenew = p1score + p1posnew

        if p1scorenew >= 21:
            p1wins += cnt1 * cnt2 * p1cnt
#            print("level", l, "p1w!!!", cnt1, "wcnt", p1wins, "d1", draws1 ,"+", (p1r, p1cnt), "d2", draws2)
            continue

        for p2r in dicemap:
            p2cnt = dicemap[p2r]
#            print("level", l, "p2 draw", p2r, p2cnt)
            p2posnew = move(p2pos, p2r)
            p2scorenew = p2score + p2posnew

            if p2scorenew >= 21:
                p2wins += cnt1 * cnt2 * p2cnt * p1cnt
#                print("level", l, "p2w!!!", cnt2, "wcnt", p2wins, "d1", draws1, "+", (p1r, p1cnt), "d2", draws2, "+", (p2r, p2cnt))
                continue
            # d1c = copy.deepcopy(draws1)
            # d2c = copy.deepcopy(draws2)
            # d1c.append((p1r, p1cnt))
            # d2c.append((p2r, p2cnt))
            r = part2_round(l+1, dicemap, p1posnew, p2posnew, p1scorenew, p2scorenew, cnt1 * p1cnt, cnt2 * p2cnt, [],[])#d1c, d2c)
            p1wins += r[0]
            p2wins += r[1]
#    print("level", l, "ret", p1wins, p2wins)
    return (p1wins, p2wins)

def part2(p1pos, p2pos):
    c = 0
    m=defaultdict(int)
    for i,j,k in itertools.product([1,2,3], [1,2,3], [1,2,3]):
        c+=1
        s = sum([i,j,k])
        m[s]+=1
        print(i,j,k, s, c)
    print(m)
    r = part2_round(1, m, p1pos, p2pos, 0, 0, 1, 1, [], [])
    print("Part2", r, r[0] if r[0] > r[1] else r[1])


def run():
    lines = open(sys.argv[1]).read().splitlines()
    p1pos = int(re.search('(\d+)(?!.*\d)', lines[0]).group()) # last nr
    p2pos = int(re.search('(\d+)(?!.*\d)', lines[1]).group())
    print(p1pos, p2pos)
    part1(p1pos, p2pos)
    if len(sys.argv) > 2:
        part21(p1pos, p2pos)
    else:
        part2(p1pos, p2pos)

run()
