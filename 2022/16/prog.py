import sys
import re
import heapq
import itertools
import copy
import cProfile

# move: (valve, rate, tdelta)
def get_moves(mat, start, unlocked):
    visited = set()
    moves = []
    q = [(0, start)]
    while q:
        (steps, valve) = q.pop(0)
        if valve not in visited:
            visited.add(valve)
            if valve not in unlocked and mat[valve][0] != 0 and valve != start:
                moves.append((valve, mat[valve][0], steps))
            for nextv in mat[valve][1]:
                if nextv not in visited:
                    q.append((steps + 1, nextv))
    moves1 = sorted(moves, key=lambda x: x[1], reverse=True)
    return moves1

def openbrute(movemat, valve, opened, time_limit, time, open_rate, score, maxscore):
    if maxscore[0] < score:
        # print("newmax", maxscore, score, open_rate, opened)
        maxscore[0] = score

    if time >= time_limit:
        return

    moves = movemat[valve]
    opened.add(valve)
    for  m in moves:
        if m[0] not in opened:
            newr = m[1]
            tdelta = m[2]+1
            totalopen = open_rate + newr
            tremain = (time_limit - time - tdelta)
            newscore = score + newr * tremain
            openbrute(movemat, m[0], opened, time_limit, time+tdelta, totalopen, newscore, maxscore)
    opened.remove(valve)

def calc_new_params(move1, move2, time_limit, time, open_rate, score):
    # open move1
    if move1[2] < move2[2]:
        newr = move1[1]
        tdelta = move1[2]+1
        tremain = (time_limit - time - tdelta)
        newscore = score + newr * tremain
        # print("newscore m1", move1, move2, newr, "tremain", tremain, "s", score, "ns", newscore)
        move2 = (move2[0], move2[1], move2[2]- tdelta)
        return (move1, move2, True, False, newscore, time+tdelta, open_rate + newr)
    # open move1 & move2
    elif move1[2] == move2[2]:
        newr = move1[1] + move2[1]
        tdelta = move1[2]+1
        tremain = (time_limit - time - tdelta)
        newscore = score + newr * tremain
        return (move1, move2, True, True, newscore, time+tdelta, open_rate + newr)
    # open move2
    else:
        newr = move2[1]
        tdelta = move2[2]+1
        tremain = (time_limit - time - tdelta)
        newscore = score + newr * tremain
        # print("newscore m2", move1, move2, newr, "tremain", tremain, "s", score, "ns", newscore)
        move1 = (move1[0], move1[1], move1[2]- tdelta)
        return (move1, move2, False, True, newscore, time+tdelta, open_rate + newr)


# limit combinations by limiting time, probably doesn't work for all inputs
time_cutoff = 2

def openbrute2(movemat, move1, move2, finish1, finish2, opened, time_limit, time, open_rate, score, maxscore):
    global time_cutoff
    if maxscore[0] < score:
        print("newmax", maxscore[0], score, open_rate, opened, [move1[0], move2[0]], finish1, finish2,  time)
        maxscore[0] = score
    if time >= (time_limit - time_cutoff):
        return -1

    # move 2nd
    if not finish1:
        moves2 = movemat[move2[0]]
        opened.add(move2[0])
        for m2 in moves2:
            if move1[0] == m2[0]:
                continue
            if m2[0] not in opened:
                (m1n, m2n, f1, f2, scoren, timen, openraten) = calc_new_params(move1, m2, time_limit, time, open_rate, score)
                openbrute2(movemat, m1n, m2n, f1, f2, opened, time_limit, timen, openraten, scoren, maxscore)
            else:
                (m1n, m2n, f1, f2, scoren, timen, openraten) = calc_new_params(move1, ("DD", 0, 1000), time_limit, time, open_rate, score)
                openbrute2(movemat, m1n, m2n, f1, f2, opened, time_limit, timen, openraten, scoren, maxscore)
        opened.remove(move2[0])
    # move 1st
    elif not finish2:
        moves1 = movemat[move1[0]]
        opened.add(move1[0])

        for m1 in moves1:
            if move2[0] == m1[0]:
                continue
            if m1[0] not in opened:
                (m1n, m2n, f1, f2, scoren, timen, openraten) = calc_new_params(m1, move2, time_limit, time, open_rate, score)
                openbrute2(movemat, m1n, m2n, f1, f2, opened, time_limit, timen, openraten, scoren, maxscore)
            else:
                (m1n, m2n, f1, f2, scoren, timen, openraten) = calc_new_params(("DD", 0, 1000), move2, time_limit, time, open_rate, score)
                openbrute2(movemat, m1n, m2n, f1, f2, opened, time_limit, timen, openraten, scoren, maxscore)
        opened.remove(move1[0])
    # move both
    else:
        moves1 = movemat[move1[0]]
        opened.add(move1[0])
        moves2 = movemat[move2[0]]
        opened.add(move2[0])

        for m1 in moves1:
            if m1[0] not in opened:
                for m2 in moves2:
                    if m1[0] == m2[0]:
                        continue
                    if m2[0] not in opened:
                        (m1n, m2n, f1, f2, scoren, timen, openraten) = calc_new_params(m1, m2, time_limit, time, open_rate, score)
                        openbrute2(movemat, m1n, m2n, f1, f2, opened, time_limit, timen, openraten, scoren, maxscore)
                            
        opened.remove(move1[0])
        if move2[0] in opened:
            opened.remove(move2[0])

def run():
    global time_cutoff
    lines = open(sys.argv[1]).read().splitlines()
    mat = {}
    for l in lines:
        m = re.search("Valve (..) has flow rate=(\d+); .* valve?. (.*)", l)
        assert(m)
        valve = m.group(1)
        rate = int(m.group(2))
        dst = m.group(3).split(", ")
        #print(valve, rate, dst)
        mat[valve] = (rate, dst)

    moves = {}
    for k in mat.keys():
        if mat[k][0] != 0 or k == 'AA':
            moves[k] = get_moves(mat, k, set())

    opened = set()
    maxscore=[0]
    openbrute(moves, 'AA', opened, 30, 0, 0, 0, maxscore)
    print ('Part1', maxscore[0])

    maxscore=[0]
    opened = set()
    openbrute2(moves, ("AA", 0, 0), ("AA", 0, 0), True, True, opened, 26, 0, 0, 0, maxscore)

    print ('Part2', maxscore[0], time_cutoff)

run()

