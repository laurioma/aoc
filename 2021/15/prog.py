import sys
import itertools
from collections import deque

def printm(matrix):
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            print("%1d" % matrix[y][x], end='')
        print("")
 
def check_valid(mat, costmap, row, col, dist):
    return (row >= 0) and (row < len(mat)) and (col >= 0) and (col < len(mat[0])) \
            and (costmap[row][col] == 0 or costmap[row][col] > (dist + mat[row][col]))
 
def find_path(mat, src, dest):
    i, j = src
    x, y = dest
    if not mat or len(mat) == 0 or mat[i][j] == 0 or mat[x][y] == 0:
        print('error', src, dest)
        return -1
 
    q = deque()
    costmap = [[False for x in range(len(mat))] for y in range(len(mat[0]))]

    q.append((i, j, 0))
 
    min_dist = sys.maxsize

#    timer = 0
    while q:
        (i, j, dist) = q.popleft()
 
#        timer += 1
#        if timer % 100000 == 0:
#            print(i, j, dist)

        # if the destination is found, update `min_dist` and stop
        if i == x and j == y:
#            print("found new min", min_dist)
            if min_dist > dist:
                min_dist = dist
 
        dirs = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        for d in dirs:
            if check_valid(mat, costmap, i + d[1], j + d[0], dist):
                ndist = dist + mat[i + d[1]][j + d[0]]
#                print(i, j, "->", i + d[1], j + d[0], visited[i + d[1]][j + d[0]] , ndist)

                if costmap[i + d[1]][j + d[0]] > ndist or costmap[i + d[1]][j + d[0]] == 0:
                    costmap[i + d[1]][j + d[0]] = ndist
                q.append((i + d[1], j + d[0], ndist))
 
    if min_dist != sys.maxsize:
        return min_dist
    else:
        return -1

def part1():
    lines = open(sys.argv[1]).read().splitlines()

    mat = [[int(c) for c in row] for row in lines]; 
#    printm(mat)

    r = find_path(mat, (0,0), (len(mat)-1,len(mat[0])-1))
    print("Part1", r)

def part2():
    lines = open(sys.argv[1]).read().splitlines()

    mat = [[int(c) for c in row] for row in lines]; 
    maxrep = 5
    dstmat = [[0 for i in range(len(mat) * maxrep)] for j in range(len(mat[0]) * maxrep)]

    for y, x in itertools.product(range(maxrep), range(maxrep)):
        for yy, xx in itertools.product(range(len(mat)), range(len(mat[0]))):
            dstx = (x)*len(mat[0]) + xx
            dsty = (y)*len(mat) + yy
            #print(y, x, yy, xx, dstx, dsty)
            dst = (mat[yy][xx] + (x + y))
            dstmat[dsty][dstx] = dst % 9 if dst > 9 else dst

    r = find_path(dstmat, (0,0), (len(dstmat)-1,len(dstmat[0])-1))

    print("Part2", r)
        
part1() if len(sys.argv) < 3 or sys.argv[2] == "1" else part2()