import sys
from random import randrange
from collections import defaultdict
import itertools
import copy


def printm(grid):
    for r in grid:
        for c in r:
            print(c, end='')
        print("")

def step(grid):

    w = len(grid[0])
    h = len(grid)
    moves = []
    for y in range(h):
        for x in range(w):
            nextx = x+1 if x+1 < w else 0
            if grid[y][x] == '>' and grid[y][nextx] == '.':
                moves.append([y,x,nextx])
    for y,x,nextx in moves:
        grid[y][nextx] = grid[y][x]
        grid[y][x] = '.'

    moves = []
    for y in range(h):
        nexty = y+1 if y+1 < h else 0
        for x in range(w):
            if grid[y][x] == 'v' and grid[nexty][x] == '.':
                moves.append([y,x,nexty])
    for y,x,nexty in moves:
        grid[nexty][x] = grid[y][x]
        grid[y][x] = '.'

def eq(g1,g2):
    w = len(g1[0])
    h = len(g1)
    eq = True
    for y in range(h):
        for x in range(w):
            if g1[y][x] != g2[y][x]:
                eq = False
    return eq

def run(part2):
    lines = open(sys.argv[1]).read().splitlines()
    grid = [[c for c in row] for row in lines];
    i=0
    while True:
        i+=1
        print("s",i)
#        printm(grid)
        comp = copy.deepcopy(grid)
        step(grid)
        if eq(grid, comp):
            break
    print("Part1", i)
    

run(0) if len(sys.argv) < 3 or sys.argv[2] == "1" else run(1)
