import sys

def printm(matrix):
    for (i,c) in enumerate(matrix):
        if i % 40 == 0:
            print("")
        print(c, end='')

def draw(screen, cycle, X):
    screen[cycle] = '#' if cycle % 40 in [X-1, X, X+1] else '.'

def calc_strength(cycle, X, strength):
    if (cycle + 20) % 40 == 0:
        strength += cycle * X
    return strength

def run():
    lines = open(sys.argv[1]).read().splitlines()
    cmds = []
    for l in lines:
        s = l.split()
        if len(s) == 1:
            cmds.append(s)
        else:
            cmds.append([s[0], int(s[1])])

    X = 1
    cidx = 0
    cycle = 0
    strength = 0
    screen = ['.' for x in range(40*6)]

    while True:
        if len(cmds) == cidx:
            break
        cmd = cmds[cidx]

        draw(screen, cycle, X);
        cycle += 1
        strength = calc_strength(cycle, X, strength)

        if len(cmd) == 1:
            cidx += 1
            continue
        else:
            draw(screen, cycle, X);
            cycle += 1
            strength = calc_strength(cycle, X, strength)

            X += cmd[1]
            cidx += 1

    print("Part1", strength)
    printm(screen)


run()