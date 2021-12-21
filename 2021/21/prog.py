import sys
import itertools
import re
from collections import defaultdict

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

def part2_round(l, dicemap, p1pos, p2pos, p1score, p2score, cnt1, cnt2):
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
#            print("level", l, "p1w!!!", cnt1, "wcnt", p1wins)
            continue

        for p2r in dicemap:
            p2cnt = dicemap[p2r]
#            print("level", l, "p2 draw", p2r, p2cnt)
            p2posnew = move(p2pos, p2r)
            p2scorenew = p2score + p2posnew

            if p2scorenew >= 21:
                p2wins += cnt1 * cnt2 * p2cnt * p1cnt
#                print("level", l, "p2w!!!", cnt2, "wcnt", p2wins)
                continue

            r = part2_round(l+1, dicemap, p1posnew, p2posnew, p1scorenew, p2scorenew, cnt1 * p1cnt, cnt2 * p2cnt)
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

    r = part2_round(1, m, p1pos, p2pos, 0, 0, 1, 1)
    print("Part2", r, r[0] if r[0] > r[1] else r[1])


def run():
    lines = open(sys.argv[1]).read().splitlines()
    p1pos = int(re.search('(\d+)(?!.*\d)', lines[0]).group()) # last nr
    p2pos = int(re.search('(\d+)(?!.*\d)', lines[1]).group())

    part1(p1pos, p2pos)
    part2(p1pos, p2pos)

run()
