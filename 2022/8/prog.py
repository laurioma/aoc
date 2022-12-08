import sys 
import re
import itertools

def printm(matrix):
    for r in matrix:
        for c in r:
            print("%1d" % int(c), end='')
        print("")
    
def is_visible(matrix, w, h, x, y):
    if x == 0 or y == 0 or x == w-1 or y == h-1:
        return True
    visible = True
    for xx in range(x-1, -1, -1):
        if matrix[y][x] <= matrix[y][xx]:
            visible = False
            break
    if visible:
        return True
    visible = True
    for xx in range(x+1, w):
        if matrix[y][x] <= matrix[y][xx]:
            visible = False
            break
    if visible:
        return True
    visible = True
    for yy in range(y-1, -1, -1):
        if matrix[y][x] <= matrix[yy][x]:
            visible = False
            break
    if visible:
        return True
    visible = True
    for yy in range(y+1, h):
        if matrix[y][x] <= matrix[yy][x]:
            visible = False
            break
    return visible

def score(matrix, w, h, x, y):
    scorel = 0
    for xx in range(x-1, -1, -1):
        scorel += 1
        if matrix[y][x] <= matrix[y][xx]:
            break;
    scorer = 0
    for xx in range(x+1, w):
        scorer += 1
        if matrix[y][x] <= matrix[y][xx]:
            break;
    scoreu = 0
    for yy in range(y-1, -1, -1):
        scoreu += 1
        if matrix[y][x] <= matrix[yy][x]:
            break;
    scored = 0
    for yy in range(y+1, h):
        scored += 1
        if matrix[y][x] <= matrix[yy][x]:
            break;

    return scorel*scorer*scoreu*scored

def run():
    lines = open(sys.argv[1]).read().splitlines()
    matrix = [list(row) for row in lines]; w=len(matrix[0]); h=len(matrix)

    answ = 0
    for y in range(h):
        for x in range(w):
            if is_visible(matrix, w, h, x, y):
                answ+=1
    print("Part1", answ)

    answ = 0
    for y in range(h):
        for x in range(w):
            s = score(matrix, w, h, x, y)
            if s > answ:
                answ = s
    print("Part2", answ)

run()