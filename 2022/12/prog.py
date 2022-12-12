import sys

def printm(matrix):
    for r in matrix:
        for c in r:
            print(c, end='')
        print("")

def bfs(mat, start, end):
    visited = set()
    q = [(0, start)]
    while q:
        (cost, coord) = q.pop(0)
        if coord not in visited:
            visited.add(coord)

            if coord == end:
                return cost

            dirs = [(-1, 0), (0, -1), (0, 1), (1, 0)]
            for d in dirs:
                x = coord[0] + d[0]
                y = coord[1] + d[1]
                if 0 <= x < len(mat[0]) and 0 <= y < len(mat) and (x, y) not in visited and ord(mat[y][x]) - ord(mat[coord[1]][coord[0]]) <= 1:
                    nextcost = cost + 1
                    q.append((nextcost, (x, y)))
    return -1

MYPOS = 'S'
TARGET = 'E'

def run():
    lines = open(sys.argv[1]).read().splitlines()
    matrix = [list(row) for row in lines]; w=len(matrix[0]); h=len(matrix)
    mypos = (0,0)
    target = (0,0)
    for r in range(h):
        for c in range(w):
            if matrix[r][c] == MYPOS:
                mypos = (c, r)
                matrix[r][c] = 'a'
            if matrix[r][c] == TARGET:
                target = (c, r)
                matrix[r][c] = 'z'

    cost = bfs(matrix, mypos, target)
    print ('Part1', cost)

    startpos = []
    for r in range(h):
        for c in range(w):
            if matrix[r][c] == 'a':
                startpos.append((c, r))

    shortest = sys.maxsize
    for p in startpos:
        cost = bfs(matrix, p, target)
        if cost < shortest and cost != -1:
            shortest = cost 
    print ('Part2 ', shortest)

run()
