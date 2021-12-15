import sys
import itertools
import heapq

def printm(matrix):
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            print("%1d" % matrix[y][x], end='')
        print("")
 
def dijkstra(mat, start, end):
    visited = set()
    q = [(0, start)]
    while q:
        (cost, coord) = heapq.heappop(q)
        if coord not in visited:
            visited.add(coord)

            if coord == end: 
                return cost
#            print(coord, cost)
            dirs = [(-1, 0), (0, -1), (0, 1), (1, 0)]
            for d in dirs:
                x = coord[0] + d[0]
                y = coord[1] + d[1]
                if 0 <= x < len(mat[0]) and 0 <= y < len(mat) and (x, y) not in visited:
                    nextcost = cost + mat[y][x]
                    heapq.heappush(q, (nextcost, (x, y)))


def part1():
    lines = open(sys.argv[1]).read().splitlines()

    mat = [[int(c) for c in row] for row in lines]; 
#    printm(mat)

    r = dijkstra(mat, (0,0), (len(mat)-1,len(mat[0])-1))
    print("Part1", r)

def part2():
    lines = open(sys.argv[1]).read().splitlines()

    mat = [[int(c) for c in row] for row in lines]; 
    maxrep = 5
    dstmat = [[0 for i in range(len(mat) * maxrep)] for j in range(len(mat[0]) * maxrep)]

    for y, x in itertools.product(range(maxrep), range(maxrep)):
        for yy, xx in itertools.product(range(len(mat)), range(len(mat[0]))):
            dstx = x*len(mat[0]) + xx
            dsty = y*len(mat) + yy
            dst = (mat[yy][xx] + (x + y))
            dstmat[dsty][dstx] = dst % 9 if dst > 9 else dst

    r = dijkstra(dstmat, (0,0), (len(dstmat)-1, len(dstmat[0])-1))

    print("Part2", r)
        
part1() if len(sys.argv) < 3 or sys.argv[2] == "1" else part2()
