import sys 
from collections import defaultdict

def ctype(c, jokker):
    cc = defaultdict(lambda:0)
    jc = 0
    for char in c:
        if jokker and char == 'J':
            jc += 1
        else:
            cc[char] += 1
    scc = sorted(cc.values(), reverse=True)
    if jokker:
        if len(scc) == 0:
            scc.append(0)
        scc[0] += jc
    if scc[0] == 5:
        return 7
    if scc[0] == 4:
        return 6
    if scc[0] == 3 and scc[1] == 2:
        return 5
    if scc[0] == 3:
        return 4
    if scc[0] == 2 and scc[1] == 2:
        return 3
    if scc[0] == 2:
        return 2
    return 1

cardtypes = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

def geti(c, cardtypes):
    for i in range(len(cardtypes)):
        if c == cardtypes[i]:
            return len(cardtypes)-i
    assert False, "invalid card"

def subscore(card, cardtypes):
    res = 0
    for c in card:
        res *= 100
        res += geti(c, cardtypes)
    return res

def score(card):
    s1 = ctype(card[0], False)
    s2 = subscore(card[0], cardtypes)
    return s1 * 100000000000 + s2

def part1():
    lines = open(sys.argv[1]).read().splitlines()
    cards = []
    for l in lines:
        c=l.split()
        cards.append([c[0], int(c[1])])

    scards = sorted(cards, key=lambda c: score(c))
    res = 0
    for i,c in enumerate(scards):
        res += (i+1) * c[1]

    print('Part1', res)

cardtypes2 = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']

def score2(card):
    s1 = ctype(card[0], True)
    s2 = subscore(card[0], cardtypes2)

    return s1 * 100000000000 + s2

def part2():
    lines = open(sys.argv[1]).read().splitlines()
    cards = []
    for l in lines:
        c=l.split()
        cards.append([c[0], int(c[1])])

    scards = sorted(cards, key=lambda c: score2(c))
    res = 0
    for i,c in enumerate(scards):
        res += (i+1) * c[1]

    print('Part2', res)

part1()
part2()