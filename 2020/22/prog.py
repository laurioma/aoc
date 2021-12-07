import sys
import time
import copy
import re
import itertools
from collections import defaultdict

def part1(cards1, cards2):
    roundnr = 1
    while cards1 and cards2:
        print ("Round", roundnr)
        roundnr +=1 
        c1 = cards1.pop(0)
        c2 = cards2.pop(0)
        print ("p1", c1, " c ", cards1)
        print ("p2", c2, " c ", cards2)
        if c1 > c2:
            cards1.append(c1)
            cards1.append(c2)
        else:
            cards2.append(c2)
            cards2.append(c1)

    if cards2:
        cards = cards2
    else:
        cards = cards1
    answer = 0
    idx = 1
    print("cards", cards)
    while cards:
        c = cards.pop()
        print(idx, c, answer)
        answer += c * idx
        idx +=1
    print("Answer1", answer)

gamenr = 1

def game2(cards1, cards2):
    global gamenr
    gnr = gamenr
    gamenr +=1
    orders = set()
    roundnr = 1
    while cards1 and cards2:
#        print ("Game", gnr, "Round", roundnr)
        roundnr +=1 
        ch = (tuple(cards1), tuple(cards2))
        if ch in orders:
#            print("ORDER HAPPENED Player 1 wins!", ch, orders)
            return True
        else:
#            print("orders!", ch, " ", orders)
            orders.add(ch)
        c1 = cards1.pop(0)
        c2 = cards2.pop(0)

#        print ("p1", c1, " c ", cards1)
#        print ("p2", c2, " c ", cards2)

        if len(cards1) >= c1 and len(cards2) >= c2:
            if game2(cards1[:c1].copy(), cards2[0:c2].copy()):
                cards1.append(c1)
                cards1.append(c2)
            else:
                cards2.append(c2)
                cards2.append(c1)
        else:
            if c1 > c2:
                cards1.append(c1)
                cards1.append(c2)
            else:
                cards2.append(c2)
                cards2.append(c1)
    # return true if p1 won
    return bool(cards1)

def part2(cards1, cards2):
    if game2(cards1, cards2):
        cards = cards1
    else:
        cards = cards2
    answer = 0

    idx = len(cards)
    print("cards", cards)
    for c in cards:
        answer += c * idx
        idx -=1
    print("Answer2", answer)

# find all lines containi
def execute(file, partnr):
    global nump
    data = ""
    with open(file) as f:
        data = f.read()

    rows = data.split('\n')

    cards1 = []
    cards2 = []
    playerNr = 0
    for r in rows:
        if r == "":
            continue
        if re.search("Player \d", r):
            playerNr +=1
        else:
            if playerNr == 1:
                cards1.append(int(r))
            else:
                cards2.append(int(r))


    if partnr == 0:
        part1(cards1, cards2)
    else:
        part2(cards1, cards2)


f = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
p2 = 0 if len(sys.argv) < 3 else int(sys.argv[2])
print ("P2", p2)
execute(f, p2)