import sys 
from collections import defaultdict
import heapq

def printm(matrix, path=None):
    for y,r in enumerate(matrix):
        for x,c in enumerate(r):
            if path != None and (x, y) in path:
                print('#', end='')
            else:
                print(c, end='')
        print("")

def dir(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])

def straight_len(path):
    if len(path) < 1:
        return 1
    slen = 0
    pdir = None
    for c in range(1, len(path)):
        ndir = dir(path[-c], path[-(c+1)])
        if pdir != None and pdir != ndir:
            break
        slen += 1
        pdir = ndir
    return slen

def checkstep(path, coord):
    # don't step back
    if len(path) > 1 and path[-2] == coord:
        return False
    if straight_len(path + [coord]) >= 4:
        return False
    return True 

def dijkstra(mat, start, end, check_f, hist_len):
    visited = set()

    q = [(0, start, [start])]
    while q:
        (cost, coord, path) = heapq.heappop(q)
        hist = tuple(path[-hist_len:])

        if (coord, hist) not in visited:
            visited.add((coord, hist))

            if coord == end:
                # part2 extra check
                if hist_len > 4:
                    slen = straight_len(path)
                    if slen >= 4 and slen <= 10:
                        return cost, path
                else:
                    return cost, path
            dirs = [(-1, 0), (0, -1), (0, 1), (1, 0)]
            for d in dirs:
                x = coord[0] + d[0]
                y = coord[1] + d[1]
                if 0 <= x < len(mat[0]) and 0 <= y < len(mat) and (x, y) not in visited and check_f(path, (x,y)):
                    nextcost = cost + int(mat[y][x])
                    npath = path[:]
                    npath.append((x,y))
                    heapq.heappush(q, (nextcost, (x, y), npath))
    return -1, []

def part1():
    lines = open(sys.argv[1]).read().splitlines()
    matrix = [row for row in lines]
    start = (0,0)
    end = (len(matrix[0])-1, len(matrix)-1)
    c, v = dijkstra(matrix, start, end, checkstep, 4)
#    printm(matrix, v)
    print('Part1', c)

def checkstep2(path, coord):
    # don't step back
    if len(path) > 1 and path[-2] == coord:
        return False
    slen = straight_len(path)
    if slen >= 10:
        pdir = dir(path[-1], path[-2])
        ndir = dir(coord, path[-1])
        return ndir != pdir
    if slen < 4 and len(path) > 1 :
        pdir = dir(path[-1], path[-2])
        ndir = dir(coord, path[-1])
        return ndir == pdir
    return True

def part2():
    lines = open(sys.argv[1]).read().splitlines()
    matrix = [row for row in lines]
    start = (0,0)
    end = (len(matrix[0])-1, len(matrix)-1)
    c, v = dijkstra(matrix, start, end, checkstep2, 10)
#    printm(matrix, v)
    print('Part2', c)

part1()
part2()
