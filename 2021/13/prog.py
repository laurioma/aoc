import sys

def printp(coords):
    maxx = 0
    maxy = 0
    for c in coords:
        if c[0] > maxx:
            maxx = c[0]
        if c[1] > maxy:
            maxy = c[1]
    for y in range(maxy+1):
        for x in range(maxx+1):
            if (x,y) in coords:
                print('#', end='')
            else:
                print('.', end='')
        print("")

def foldy(coords, y):
    remove = []
    add = []
    for c in coords:
        if c[1] > y:
            remove.append(c)
            dst = c[1] - y 
#            print ('foldy', coords[i], dst, y - dst)
            add.append((c[0], y - dst))
    for r in remove:
        coords.remove(r)
    for a in add:
        coords.add(a)

def foldx(coords, x):
    remove = []
    add = []
    for c in coords:
        if c[0] > x:
            remove.append(c)
            dst = c[0] - x 
#            print ('foldx', coords[i], dst, y - dst)
            add.append((x - dst, c[1]))
    for r in remove:
        coords.remove(r)
    for a in add:
        coords.add(a)

def run(part2):
    lines = open(sys.argv[1]).read().splitlines()
    instr = []
    getinstr = False
    coords = set()
    for l in lines:
        if l.strip() == "":
            getinstr = True
            continue

        if not getinstr:
            s = l.split(',')
            coords.add((int(s[0]), int(s[1])))

        else:
            i = l.split('=')
            instr.append((i[0], int(i[1])))

    if not part2:
#        print("instr", instr[0])
        if instr[0][0] == "fold along x":
            foldx(coords, instr[0][1])
        else:
            foldy(coords, instr[0][1])

        print("Part1", len(coords))
    else:
        for i in instr:
#            print("instr", i)
            if i[0] == "fold along x":
                foldx(coords, i[1])
            else:
                foldy(coords, i[1])
        printp(coords)

run(0) if len(sys.argv) < 3 or sys.argv[2] == "1" else run(1)