import sys

def printm(rope, tl, br):
    for y in range(tl[1], br[1]+1):
        for x in range(tl[0], br[0]+1):
            for i in range(len(rope)):
                if [x,y] == rope[i]:    
                    if i == 0:
                        print('H', end='')
                    elif i == len(rope)-1:
                        print('T', end='')
                    else:
                        print(i, end='')
                    break
            else:
                print('.', end='')
        print("")

def step_head(H, dir):
    if dir =='R':
        H[0] += 1
    elif dir == 'L':
        H[0] -= 1
    elif dir == 'U':
        H[1] -= 1
    elif dir == 'D':
        H[1] += 1
    else:
        assert(False)

def step_tail(H, T):
    assert(abs(H[0]-T[0]) <= 2)
    assert(abs(H[1]-T[1]) <= 2)

    if abs(H[0]-T[0]) == 2 and abs(H[1]-T[1]) == 2:
        T[0] += 1 if H[0]>T[0] else -1
        T[1] += 1 if H[1]>T[1] else -1
    elif abs(H[0]-T[0]) == 2:
        T[0] += 1 if H[0]>T[0] else -1
        T[1] = H[1]
    elif abs(H[1]-T[1]) == 2:
        T[1] += 1 if H[1]>T[1] else -1
        T[0] = H[0]

def step(rope, dir):
    step_head(rope[0], dir)
    for i in range(len(rope)-1):
        step_tail(rope[i], rope[i+1])

def run():
    lines = open(sys.argv[1]).read().splitlines()
    cmds = []
    for l in lines:
        s = l.split()
        cmds.append((s[0], int(s[1])))

    rope=[[0,0], [0,0]]
    # tl = (-5,-5)
    # br=(5,5)
    tailpos = {}
    for c in cmds:
        assert(c[1]> 0)
        for i in range(c[1]):
            step(rope, c[0])
            tailpos[(rope[1][0], rope[1][1])] = True
#            print("cmd", c, i)
            #printm(rope, tl, br)
    print("Part1", len(tailpos))
    rope = []
    for _ in range(10):
        rope.append([0,0])
    tailpos = {}
    for c in cmds:
        assert(c[1]> 0)
        for i in range(c[1]):
            step(rope, c[0])
            tailpos[(rope[-1][0], rope[-1][1])] = True
            #print("cmd", c, i)
            #printm(rope, tl, br)
    print("Part2", len(tailpos))


run()