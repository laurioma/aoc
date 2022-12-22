import sys
import re

FACING_U=3 
FACING_L=2
FACING_D=1
FACING_R=0

def printm(img, pos, path):
    for y in range(len(img)):
        for x in range(len(img[0])):
            hadpath = False
            for (xx,yy,f) in path:
                if x == xx and y == yy:
                    hadpath = True
                    print(facingch(f), end='')
                    assert(img[y][x] != '#')
                    break
            if not hadpath:  
                if (x, y) == pos:
                    print('X', end='')
                else:
                    print(img[y][x], end='')

        print("")

def row_bounds(matrix, row):
    xmin = sys.maxsize
    xmax = -sys.maxsize
    for x in range(len(matrix[row])):
        if matrix[row][x] != ' ':
            xmin = min(xmin, x)
            xmax = max(xmax, x)
    return (xmin, xmax)

def col_bounds(matrix, col):
    ymin = sys.maxsize
    ymax = -sys.maxsize
    for y in range(len(matrix)):
        if matrix[y][col] != ' ':
            ymin = min(ymin, y)
            ymax = max(ymax, y)
    return (ymin, ymax)

def facingch(facing):
    if facing == FACING_U:
        return '|'
    if facing == FACING_L:
        return '<'
    if facing == FACING_D:
        return 'v'
    if facing == FACING_R:
        return '>'

def turn(facing, rot):
    assert(facing >= 0 and facing < 4)
    if rot == 'L':
        return facing - 1 if facing > 0 else 3
    elif rot == 'R':
        return facing + 1 if facing < 3 else 0


def run():
    input = open(sys.argv[1]).read().split('\n\n')

    lines=input[0].splitlines()
    matrix=[]
    h = len(lines[0])
    for line in lines:
        row = []
        for x in range(h):
            if len(line) > x:
                row.append(line[x])
            else:
                row.append(' ')
        matrix.append(row)

    currpos = ()
    for x in range(len(matrix[0])):
        if matrix[0][x] != ' ':
            currpos = (x, 0)
            break

    cmds = []
    cmdstr = "R"+input[1]
    for cs in re.findall('[RL]\d+', cmdstr):
        cmds.append((cs[0], int(cs[1:])))

    facing = FACING_U #compensate added R
    path=[]
    for ci, cmd in enumerate(cmds):
        facing = turn(facing, cmd[0])
        if facing==FACING_R:
            (xmin, xmax) = row_bounds(matrix, currpos[1])
            for i in range(cmd[1]):
                newx = currpos[0] + 1
                if newx == xmax+1:
                    newx=xmin
                if matrix[currpos[1]][newx] == '.':
                    path.append((newx, currpos[1], facing))
                    currpos = (newx, currpos[1])
        elif facing==FACING_L:
            for i in range(cmd[1]):
                xmin, xmax = row_bounds(matrix, currpos[1])
                newx = currpos[0] - 1
                if newx == xmin-1:
                    newx = xmax
                if matrix[currpos[1]][newx]  == '.':
                    path.append((newx, currpos[1], facing))
                    currpos = (newx, currpos[1])
        elif facing==FACING_U:
            for i in range(cmd[1]):
                ymin, ymax = col_bounds(matrix, currpos[0])
                newy = currpos[1] - 1
                if newy == ymin-1:
                    newy = ymax
                if matrix[newy][currpos[0]]  == '.':
                    path.append( (currpos[0], newy, facing))
                    currpos = (currpos[0], newy)
        elif facing==FACING_D:
            ymin, ymax = col_bounds(matrix, currpos[0])
            for i in range(cmd[1]):
                newy = currpos[1] + 1
                if newy == ymax+1:
                    newy = ymin
                if matrix[newy][currpos[0]] == '.':
                    path.append((currpos[0], newy, facing))
                    currpos = (currpos[0], newy)
        else:
            assert(False)

        # printm(matrix, currpos, path)
    print("Part1", (currpos[1]+1) * 1000 + (currpos[0]+1)*4+facing)
run()

