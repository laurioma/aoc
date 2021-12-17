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
    print("xrange", range(minx, maxx), "yrange", range(miny, maxy), pos)
    for y in range(maxy, miny-1, -1):
        for x in range(minx, maxx+1):
            if (x,y) in pos:
                print('#', end='')
            elif x >= x1 and y >= y1 and x <= x2 and y <= y2 :
                print('T', end='')
            else:
                print('.', end='')
        print("")

def in_target_area(pos, x1, x2, y1, y2):
    if pos[0] in range(x1,x2+1) and pos[1] in range(y2, y1-1, -1):
        return True
    return False

def run():
    lines = open(sys.argv[1]).read().splitlines()
    x = re.search("target area: x=([0-9-]*)..([0-9-]*), y=([0-9-]*)..([0-9-]*)", lines[0])
    x1 = int(x.group(1))
    x2 = int(x.group(2))
    y1 = int(x.group(3))
    y2 = int(x.group(4))
    besty = -1000000
    bestvel = (-1, -1)
    targets = []
    for startvy in range(y1, -y1):
        for startvx in range(0, x2+1):
            pos = (0,0)
            posl = [pos]
            velx = startvx
            vely = startvy
#            print("running sim", velx, vely, pos[0], x2, pos[1], y2)
            maxy = -1000000
            while pos[0] <= x2 and pos[1] >= y1:
#                print ("pos", pos)
                posx = pos[0] + velx
                velx += (1 if velx < 0 else -1 if velx > 0 else 0)
                posy = pos[1] + vely
                vely -= 1
                pos = (posx, posy)
                if pos[1] > maxy:
                    maxy = pos[1]
#                print ("pos2", pos)
                posl.append(pos)
#                printarea(x1,x2,y1,y2, posl)
                if in_target_area(pos, x1,x2,y1,y2):
                    if besty < maxy:
                        besty = maxy
                        bestvel = (startvx, startvy)
#                    print("in target", maxy, besty, bestvel, startvx, startvy)
                    targets.append((startvx, startvy))
                    break


    print("Part1", besty)
    targets.sort()
    print("Part2", len(targets))

run()