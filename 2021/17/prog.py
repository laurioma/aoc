import sys
import itertools
import re

def printarea(x1, x2, y1, y2, pos):
    xlist = [0, x1, x2]
    ylist = [0, y1, y2]
    for p in pos:
        xlist.append(p[0])
        ylist.append(p[1])
    minx = min(xlist)
    miny = min(ylist)
    maxx = max(xlist)
    maxy = max(ylist)
    for y in range(maxy, miny-1, -1):
        for x in range(minx, maxx+1):
            if (x,y) in pos:
                print('#', end='')
            elif x >= x1 and y >= y1 and x <= x2 and y <= y2 :
                print('T', end='')
            else:
                print('.', end='')
        print("")

def run():
    lines = open(sys.argv[1]).read().splitlines()
    x = re.findall("[0-9-]+", lines[0])
    x1 = int(x[0])
    x2 = int(x[1])
    y1 = int(x[2])
    y2 = int(x[3])

    besty = -sys.maxsize
    targets = []
    for startvel in itertools.product(range(0, x2+1), range(y1, -y1)):
        pos = (0,0)
        posl = [pos]
        vel = startvel
    #    print("running sim", velx, vely, pos[0], x2, pos[1], y2)
        maxy = -sys.maxsize
        while pos[0] <= x2 and pos[1] >= y1:
            pos = (pos[0] + vel[0], pos[1] + vel[1])
            if pos[1] > maxy:
                maxy = pos[1]
            posl.append(pos)
            vel = (vel[0] - 1 if vel[0] > 0 else vel[0], vel[1] - 1)

        #    printarea(x1,x2,y1,y2, posl)
            if x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2:
                if besty < maxy:
                    besty = maxy
                # print("in target", maxy, besty, startvx, startvy)
                targets.append(startvel)
                break


    print("Part1", besty)
    print("Part2", len(targets))

run()