import sys 
from collections import defaultdict

def printm(matrix, visited=None):
    for y,r in enumerate(matrix):
        for x,c in enumerate(r):
            if visited != None and (x, y) in visited:
                print('#', end='')
            else:
                print(c, end='')
        print("")

def runbeam(matrix, visited, pos, dir, lvl):
    while True:
        if (pos[0], pos[1]) in visited and dir in visited[(pos[0], pos[1])]:
            break
        visited[(pos[0], pos[1])].append(dir)

        if matrix[pos[1]][pos[0]] == '/':
            if dir == 'r':
                dir = 'u'
            elif dir == 'd':
                dir = 'l'
            elif dir == 'l':
                dir = 'd'
            elif dir == 'u':
                dir = 'r'
        elif matrix[pos[1]][pos[0]] == '\\':
            if dir == 'r':
                dir = 'd'
            elif dir == 'd':
                dir = 'r'
            elif dir == 'l':
                dir = 'u'
            elif dir == 'u':
                dir = 'l'
        elif matrix[pos[1]][pos[0]] == '|':
            if dir == 'r' or dir == 'l':
                npos = pos[:]
                runbeam(matrix, visited, npos, 'u', lvl+1)
                npos = pos[:]
                runbeam(matrix, visited, npos, 'd', lvl+1)
                break
        elif matrix[pos[1]][pos[0]] == '-':
            if dir == 'u' or dir == 'd':
                npos = pos[:]
                runbeam(matrix, visited, npos, 'l', lvl+1)
                npos = pos[:]
                runbeam(matrix, visited, npos, 'r', lvl+1)
                break

        if dir == 'u':
            pos[1] -= 1
        elif dir == 'd':
            pos[1] += 1
        elif dir == 'l':
            pos[0] -= 1
        elif dir == 'r':
            pos[0] += 1
        if pos[0] < 0 or pos[0] >= len(matrix[0]) or pos[1] < 0 or pos[1] >= len(matrix):
            break
def part1():
    lines = open(sys.argv[1]).read().splitlines()
    matrix = [list(row) for row in lines]; w=len(matrix[0]); h=len(matrix)
    visited = defaultdict(list)
    runbeam(matrix, visited, [0,0], 'r', 0)
    #printm(matrix, visited)

    print('Part1', len(visited))


def part2():
    lines = open(sys.argv[1]).read().splitlines()
    matrix = [list(row) for row in lines]; w=len(matrix[0]); h=len(matrix)
    #top row
    maxlen = 0
    for x in range(w):
        visited = defaultdict(list)
        runbeam(matrix, visited, [x, 0], 'd', 0)
        if maxlen < len(visited):
            maxlen = len(visited)
    for x in range(w):
        visited = defaultdict(list)
        runbeam(matrix, visited, [x, h-1], 'u', 0)
        if maxlen < len(visited):
            maxlen = len(visited)   
    for y in range(h):
        visited = defaultdict(list)
        runbeam(matrix, visited, [0, y], 'r', 0)
        if maxlen < len(visited):
            maxlen = len(visited)  
    for y in range(h):
        visited = defaultdict(list)
        runbeam(matrix, visited, [w-1, y], 'l', 0)
        if maxlen < len(visited):
            maxlen = len(visited)
    print('Part2', maxlen)

part1()
part2()
