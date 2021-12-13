import sys

def printm(matrix):
    for r in matrix:
        for c in r:
            print(c, end='')
        print("")

def printp(coords):
    maxx = 0
    maxy = 0
    for c in coords:
        if c[0] > maxx:
            maxx = c[0]
        if c[1] > maxy:
            maxy = c[1]
    paper = [['#' if (x, y) in coords else '.' for x in range(maxx+1)] for y in range(maxy+1)]
    printm(paper)

def foldy(coords, y):
    for i in range(len(coords)):
        if coords[i][1] > y:
            dst = coords[i][1] - y 
#            print ('foldy', coords[i], dst, y - dst)
            coords[i] = (coords[i][0], y - dst)

def foldx(coords, x):
    for i in range(len(coords)):
        if coords[i][0] > x:
            dst = coords[i][0] - x 
#            print ('foldx', coords[i], dst, x - dst)
            coords[i] = (x - dst, coords[i][1])

def run(part2):
    lines = open(sys.argv[1]).read().splitlines()
    instr = []
    getinstr = False
    coords = []
    for l in lines:
        if l.strip() == "":
            getinstr = True
            continue

        if not getinstr:
            s = l.split(',')
            coords.append((int(s[0]), int(s[1])))

        else:
            i = l.split('=')
            instr.append((i[0], int(i[1])))

    if not part2:
#        print("instr", instr[0])
        if instr[0][0] == "fold along x":
            foldx(coords, instr[0][1])
        else:
            foldy(coords, instr[0][1])
        uniq = set()
        for c in coords:
            uniq.add(c)

        print("Part1", len(uniq))
    else:
        for i in instr:
#            print("instr", i)
            if i[0] == "fold along x":
                foldx(coords, i[1])
            else:
                foldy(coords, i[1])
        printp(coords)

run(0) if len(sys.argv) < 3 or sys.argv[2] == "1" else run(1)