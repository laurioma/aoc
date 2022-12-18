import sys
import itertools

def exposed_sides(cubesm, c):
    area = 0;
    if (c[0]+1, c[1], c[2]) not in cubesm:
        area += 1
    if (c[0], c[1]+1, c[2]) not in cubesm:
        area += 1
    if (c[0], c[1], c[2]+1) not in cubesm:
        area += 1
    if (c[0]-1, c[1], c[2]) not in cubesm:
        area += 1
    if (c[0], c[1]-1, c[2]) not in cubesm:
        area += 1
    if (c[0], c[1], c[2]-1) not in cubesm:
        area += 1

    return area

def touching_sides(cubesm, c):
    area = 0;
    if (c[0]+1, c[1], c[2]) in cubesm:
        area += 1
    if (c[0], c[1]+1, c[2]) in cubesm:
        area += 1
    if (c[0], c[1], c[2]+1) in cubesm:
        area += 1
    if (c[0]-1, c[1], c[2]) in cubesm:
        area += 1
    if (c[0], c[1]-1, c[2]) in cubesm:
        area += 1
    if (c[0], c[1], c[2]-1) in cubesm:
        area += 1

    return area

def count_ext_edge_area(cubesm, outside):
    visited = set()
    area = 0
    q = [outside]
    while q:
        coord = q.pop(0)
        if coord not in visited:
            visited.add(coord)

            area += touching_sides(cubesm, coord)

            # first check 6 side spaces
            dirs = [(-1, 0, 0), (0, -1, 0), (0, 0, -1), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
            for (x, y, z) in dirs:
                ncoord = (coord[0] + x, coord[1] + y, coord[2] + z)
                if ncoord not in cubesm:
                    if touching_sides(cubesm, ncoord) > 0:
                        q.append(ncoord)
                    # now check 4 spaces next to each side space
                    dirs1 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
                    for (a, b) in dirs1:
                        ncoord1 = (0,0,0)
                        if x != 0:
                            ncoord1 = (ncoord[0],ncoord[1]+a,ncoord[2]+b)
                        elif y != 0:
                            ncoord1 = (ncoord[0]+a, ncoord[1],ncoord[2]+b)
                        elif z != 0:
                            ncoord1 = (ncoord[0]+a, ncoord[1]+b, ncoord[2])
                        if ncoord1 not in cubesm:
                            if touching_sides(cubesm, ncoord1) > 0:
                                q.append(ncoord1)
                    

    return area


def run():
    lines = open(sys.argv[1]).read().splitlines()
    cubesm = {}
    minx = sys.maxsize
    outside = (0,0,0)
    for l in lines:
        c = tuple(map(int, l.split(",")))
        cubesm[c] = 1
        if minx > c[0]:
            minx = c[0]
            outside = (c[0]-1, c[1], c[2])

    area = 0
    for c in cubesm:
        area += exposed_sides(cubesm, c)
    print("Part1: ", area)

    area = count_ext_edge_area(cubesm, outside)
    print("Part2: ", area)


run()