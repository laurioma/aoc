import sys 
import os

#colors
os.system("")

def printm(matrix):
    for r in matrix:
        for c in r:
            print("%1d" % int(c), end='')
        print("")

def printm2(matrix, lows):
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if (x, y) in lows:
                print("\33[32m%1d\033[37m" % int(matrix[y][x]), end='')
            else:
                print("%1d" % int(matrix[y][x]), end='')
        print("")

def checklow2(matrix, w, h, x, y):
    islow = True
    chkcoords = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
    for xy in chkcoords:
        if xy[0] >= 0 and xy[1] >= 0 and xy[0] < w and xy[1] < h:
            if matrix[y][x] >= matrix[xy[1]][xy[0]]:
                islow = False
    return islow

def calcbasin(matrix, w, h, x, y, checked):
    checked.append((x, y))
    size = 1
    chkcoords = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
    for xy in chkcoords:
        if xy[1] >= 0 and xy[0] >= 0 and xy[1] < h and xy[0] < w and (xy[0], xy[1]) not in checked:
            if matrix[xy[1]][xy[0]] != '9':
                size += calcbasin(matrix, w, h, xy[0], xy[1], checked)
    return size

def run(part2):
    lines = open(sys.argv[1]).read().splitlines()
    matrix = [list(row) for row in lines]; w=len(matrix[0]); h=len(matrix)
    #printm(matrix)

    lowpoints = []
    for y in range(h):
        for x in range(w):
            if checklow2(matrix, w, h, x, y):
                lowpoints.append((x, y))
    #print (lowpoints)
    sum = 0
    for xy in lowpoints:
        sum += (int(matrix[xy[1]][xy[0]]) + 1)
    print("Part1", sum)
    #printm2(matrix, lowpoints)

    if not part2:
        return

    sizes = []
    for xy in lowpoints:
        checked = []
        sz = calcbasin(matrix, w, h, xy[0], xy[1], checked)
        sizes.append(sz)
        #print(xy, sz)
    sizes.sort(reverse=True)
    print("Part2", sizes[0]*sizes[1]*sizes[2])

run(0) if len(sys.argv) < 3 or sys.argv[2] == "1" else run(1)

