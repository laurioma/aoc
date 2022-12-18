import sys
import re

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

def openbrute(movemat, valve, opened, time_limit, time, open_rate, score, maxscore, skipgates):
    if maxscore[0] < score:
        # print("newmax", maxscore, score, open_rate, opened)
        maxscore[0] = score

    if time >= time_limit:
        return

    moves = movemat[valve]
    opened.add(valve)
    for m in moves:
        if m[0] in skipgates:
            continue
        if m[0] not in opened:
            newr = m[1]
            tdelta = m[2]+1
            totalopen = open_rate + newr
            tremain = (time_limit - time - tdelta)
            newscore = score + newr * tremain

            openbrute(movemat, m[0], opened, time_limit, time+tdelta, totalopen, newscore, maxscore, skipgates)
    opened.remove(valve)

def run():
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
    mkeys = []
    for k in mat.keys():
        if mat[k][0] != 0:
            mkeys.append(k)
        if mat[k][0] != 0 or k == 'AA':
            moves[k] = get_moves(mat, k, set())


    maxscore = [0]
    openbrute(moves, 'AA', set(), 30, 0, 0, 0, maxscore, set())
    print ('Part1', maxscore[0])

    combinations = pow(2, len(mkeys))

    maxscore = 0
    for i in range(combinations):
        skipme = set()
        skipel = set()
        for (ki, k) in enumerate(mkeys):
            if i & pow(2, ki):
                skipme.add(k)
            else:
                skipel.add(k)

        maxscore1 = [0]
        openbrute(moves, 'AA', set(), 26, 0, 0, 0, maxscore1, skipme)
        maxscore2 = [0]
        openbrute(moves, 'AA', set(), 26, 0, 0, 0, maxscore2, skipel)
        maxscore = max(maxscore, maxscore1[0]+maxscore2[0])
    print ('Part2', maxscore)

run()

