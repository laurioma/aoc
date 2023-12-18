import sys 
import itertools

def get_bounds(matrix, check=lambda map, pos: True):
    ymin = xmin = sys.maxsize
    xmax = ymax = -sys.maxsize
    for (x,y) in matrix.keys():
        if check(matrix, (x,y)):
            xmin = min(xmin, x)
            xmax = max(xmax, x)
            ymin = min(ymin, y)
            ymax = max(ymax, y)
    tl = (xmin, ymin)
    br = (xmax, ymax)
    return (tl, br)

def printm(img):
    tl, br = get_bounds(img)
    for y in range(tl[1], br[1]+1):
        for x in range(tl[0], br[0]+1):
            print(img[(x,y)] if (x, y) in img else '.', end='')    
        print(y, "")

def fill(mat):
    tl, br = get_bounds(mat)
    start = (0, 0)
    stepx = 1 if br[0] > tl[0] else -1
    stepy = 1 if br[1] > tl[1] else -1
    for x in range(tl[0], br[0]+stepx):
        if (x, tl[1] + stepy) in mat:
            start = (x+1, tl[1] + stepy)
            break
    tofill = {start}
    while True:
        newfill = set()
        for coord in tofill:
            mat[coord] = '#'

            for dy, dx in itertools.product([-1, 0, 1], [-1, 0, 1]): 
                nx = coord[0] + dx
                ny = coord[1] + dy
                if nx >= tl[0] and nx < br[0] and ny >= tl[1] and ny < br[1] and (nx, ny) not in mat:
                    newfill.add((nx, ny))
        if len(newfill) == 0:
            break
        tofill = newfill

def part1():
    lines = open(sys.argv[1]).read().splitlines()
    instr = []
    for l in lines:
        d, cnt, col = l.split()
        instr.append((d, int(cnt), col))
    mat = {}
    pos = (0,0)
    for i in instr:
        if i[0] == 'U':
            for j in range(i[1]):
                mat[(pos[0], pos[1]-j)] = '#'
            pos = (pos[0], pos[1]-i[1])
        elif i[0] == 'D':
            for j in range(i[1]):
                mat[(pos[0], pos[1]+j)] = '#'
            pos = (pos[0], pos[1]+i[1])
        elif i[0] == 'L':
            for j in range(i[1]):
                mat[(pos[0]-j, pos[1])] = '#'
            pos = (pos[0]-i[1], pos[1])
        elif i[0] == 'R':
            for j in range(i[1]):
                mat[(pos[0]+j, pos[1])] = '#'
            pos = (pos[0]+i[1], pos[1])
    fill(mat)
    print('Part1', len(mat))

def shoelace(vertices):
    numberOfVertices = len(vertices)
    sum1 = 0
    sum2 = 0

    for i in range(0,numberOfVertices-1):
        sum1 = sum1 + vertices[i][0] *  vertices[i+1][1]
        sum2 = sum2 + vertices[i][1] *  vertices[i+1][0]

    sum1 = sum1 + vertices[numberOfVertices-1][0]*vertices[0][1]   
    sum2 = sum2 + vertices[0][0]*vertices[numberOfVertices-1][1]   

    area = abs(sum1 - sum2) / 2
    return area
  
def part2():
    dirs = {0:'R',1:'D',2:'L',3:'U'}
    lines = open(sys.argv[1]).read().splitlines()
    instr = []
    for l in lines:
        d, cnt, col = l.split()
        cnt = int(col[2:7], 16)
        diridx = int(col[7])
        d = dirs[diridx]
        instr.append([d, cnt, col])

    edgelen = 0
    pos = (0,0)
    points = [pos]

    for i in instr:
        edgelen += i[1]

        if i[0] == 'U':
            pos = (pos[0], pos[1]-i[1])
        elif i[0] == 'D':
            pos = (pos[0], pos[1]+i[1])
        elif i[0] == 'L':
            pos = (pos[0]-i[1], pos[1])
        elif i[0] == 'R':
            pos = (pos[0]+i[1], pos[1])

        points.append(pos)

    ret = shoelace(points)
    print("Part2", ret + edgelen/2+1)

part1()
part2()
