import sys
import re

FACING_U=3 
FACING_L=2
FACING_D=1
FACING_R=0

def printm(cube, align, dim, currpos, path):
    for y in range(dim*4):
        prow = y // dim 
        for x in range(dim*4):
            pcol = x // dim
            side = -1  
            for j in range(len(align)):
                if align[j] == (pcol, prow):
                    side = j
                    break
            if side != -1:
                yy = y % dim
                xx = x % dim
                hadpath = False
                for (px,py,s,f) in path:
                    if xx == px and yy == py and s == side:
                        hadpath = True
                        print(facingch(f), end='')
                        assert(cube[s][py][px] != '#')
                        break
                if not hadpath:  
                    if (xx,yy,side) == currpos:
                        print("X", end='')
                    else:
                        print(cube[side][yy][xx], end='')
            else:
                print(end=' ')
        print("")

def facingch(facing):
    if facing == FACING_U:
        return '|'
    if facing == FACING_L:
        return '<'
    if facing == FACING_D:
        return 'v'
    if facing == FACING_R:
        return '>'

def abspos(align, dim, currpos):
    sidealign = align[currpos[2]]
    return (sidealign[0]*dim + currpos[0], sidealign[1]*dim + currpos[1])

def turn(facing, rot):
    assert(facing >= 0 and facing < 4)
    if rot == 'L':
        return facing - 1 if facing > 0 else 3
    elif rot == 'R':
        return facing + 1 if facing < 3 else 0

def wrap(x,y,side, dim, facing):
    if facing == FACING_R:
        if side == 1:
            return (0, y, 6), FACING_R
        elif side == 2:
            return (y, dim-1, 5), FACING_U
        elif side == 3:
            return (0, y, 5), FACING_R
        elif side == 4:
            return (y, x, 6), FACING_U
        elif side == 5:
            return (dim-1, dim-1 - y, 6), FACING_L
        elif side == 6:
            return (dim-1, dim-1 - y, 5), FACING_L
        else:
            assert(False)
    elif facing == FACING_D:
        if side == 1:
            return (x, 0, 4), FACING_D
        elif side == 2:
            return (x, 0, 6), FACING_D
        elif side == 3:
            return (x, 0, 2), FACING_D
        elif side == 4:
            return (x, 0, 5), FACING_D
        elif side == 5:
            return (dim-1, x, 2), FACING_L
        elif side == 6:
            return (dim-1, x, 4), FACING_L
        else:
            assert(False)
    elif facing == FACING_L:
        if side == 1:
            return (0, dim-1 - y, 3), FACING_R
        elif side == 2:
            return (y, 0, 1), FACING_D
        elif side == 3:
            return (0, dim-1 - y, 1), FACING_R
        elif side == 4:
            return (y, 0, 3), FACING_D
        elif side == 5:
            return (dim-1, y, 3), FACING_L
        elif side == 6:
            return (dim-1, y, 1), FACING_L
        else:
            assert(False)
    elif facing == FACING_U:
        if side == 1:
            return (0, x, 2), FACING_R
        elif side == 2:
            return (x, dim-1, 3), FACING_U
        elif side == 3:
            return (0, x, 4), FACING_R
        elif side == 4:
            return (x, dim-1, 1), FACING_U
        elif side == 5:
            return (x, dim-1, 4), FACING_U
        elif side == 6:
            return (x, dim-1, 2), FACING_U
        else:
            assert(False)
    else:
        assert(False)

def run():
    assert(sys.argv[1] != "test.txt"), "test no longer working"

    input = open(sys.argv[1]).read().split('\n\n')
    lines=input[0].splitlines()
    dim=sys.maxsize
    for l in lines:
        lw = 0
        for c in l:
            if c != ' ':
                lw+=1
        dim = min(dim, lw)

    cube = []
    cube.append([]) #dummy to make numbers match
    for _ in range(6):
        c=[]
        for _ in range(dim):
            c.append([0]*dim)
        cube.append(c)
    

    # align = [(-1,-1), (2,0), (0,1), (1,1), (2,1), (2,2), (3,2)] 
    align = [(-1,-1), (1,0), (0,3), (0,2), (1,1), (1,2), (2,0)]
    for y,l in enumerate(lines):
        prow = y // dim 
        for x,c in enumerate(l):
            pcol = x // dim
            side = -1
            for j in range(len(align)):
                if align[j] == (pcol, prow):
                    side = j
                    break
            if side != -1:
                yy = y % dim
                xx = x % dim
                assert(side != 0)
                cube[side][yy][xx] = c
            else:
                assert(c == ' ')

    cmds = []
    cmdstr = "R"+input[1]
    for cs in re.findall('[RL]\d+', cmdstr):
        cmds.append((cs[0], int(cs[1:])))

    facing = FACING_U #compensate added R
    side = 1
    path=[]
    currpos = (0,0,1) # upper corner of side 1
    for ci, cmd in enumerate(cmds):
        facing = turn(facing, cmd[0])
        for i in range(cmd[1]):
            if facing==FACING_R:
                newpos = (currpos[0]+1, currpos[1], currpos[2])
                newf = facing
                if newpos[0] == dim:
                    newpos, newf = wrap(*currpos, dim, facing) 
                if cube[newpos[2]][newpos[1]][newpos[0]] == '.':
                    currpos = newpos
                    facing = newf
                    path.append((*newpos, newf))
            elif facing==FACING_L:
                newpos = (currpos[0]-1, currpos[1], currpos[2])
                newf = facing
                if newpos[0] == -1:
                    newpos, newf = wrap(*currpos, dim, facing)
                if cube[newpos[2]][newpos[1]][newpos[0]] == '.':
                    currpos = newpos
                    facing = newf
                    path.append((*newpos, newf))
            elif facing==FACING_U:
                newpos = (currpos[0], currpos[1]-1, currpos[2])
                newf = facing
                if newpos[1] == -1:
                    newpos, newf = wrap(*currpos, dim, facing)
                    
                if cube[newpos[2]][newpos[1]][newpos[0]] == '.':
                    currpos = newpos
                    facing = newf
                    path.append((*newpos, newf))
            elif facing==FACING_D:
                newpos = (currpos[0], currpos[1]+1, currpos[2])
                newf = facing
                if newpos[1] == dim:
                    newpos, newf = wrap(*currpos, dim, facing)
                    
                if cube[newpos[2]][newpos[1]][newpos[0]] == '.':
                    currpos = newpos
                    facing = newf
                    path.append((*newpos, newf))
            else:
                assert(False)
        #printm(cube, align, dim, currpos, path)

    col, row = abspos(align, dim, currpos)
    print("Part1", (row) * 1000 + (col+1)*4+facing, facing)

run()

