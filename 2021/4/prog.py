import sys 

def calcscore(grid, check, check_nr):
    score = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if check[r][c] != -1:
                score += int(grid[r][c])
    print("score", score, int(check_nr),"ret", score * int(check_nr))

def check_end(gn, grids, checks, check_nr, part2, winned):
    if part2:
        winned.append(gn)
        print("win nr", check_nr, gn, len(winned), winned)
        if len(winned) == len(grids):
            calcscore(grids[gn], checks[gn], check_nr)
            return 1
    else:
        calcscore(grids[gn], checks[gn], check_nr)
        return 1

def printgrid(grid):
    for r in grid:
        for c in r:
            print(" %2d" % int(c), end='')
        print("")

def run(part2):
    print ("part2",part2)
    with open(sys.argv[1]) as f:
        data = f.read()
    chunks = data.split('\n\n')
    numbers = chunks[0].split(",")
    chunks.pop(0)

    grids = []
    checks = []
    for c in chunks:
        numrows = c.split('\n')
        grid = []
        check = []
        for nr in numrows:
            grid.append(list(nr.split()))
            check.append([0]*len(grid[0]))
        grids.append(grid)
        checks.append(check)
    print(len(grids))

    winned = []
    for check_nr in numbers:
        for gn in range(len(grids)):
            for gr in range(len(grids[gn])):
                for n in range(len(grids[gn][gr])):
                    if grids[gn][gr][n] == check_nr:
                        checks[gn][gr][n] = -1

        for gn in range(len(grids)):
            if gn in winned:
                continue
#            printgrid(grids[gn])
#            printgrid(checks[gn])

            # check rows
            rowwin = 0
            for gr in range(len(grids[gn])):
                allset = 1
                for n in range(len(grids[gn][gr])):
                    if checks[gn][gr][n] == 0:
                        allset = 0
                        break
                if allset == 1:
                    print("rowwin")
                    rowwin = 1
                    if check_end(gn, grids, checks, check_nr, part2, winned):
                        return
            if not rowwin:
                # check cols
                for gc in range(len(grids[gn][0])):
                    allset = 1
                    for n in range(len(grids[gn])):
                        if checks[gn][n][gc] == 0:
                            allset = 0
                            break
                    if allset == 1:
                        print("colwin")
                        if check_end(gn, grids, checks, check_nr, part2, winned):
                            return

run(0) if len(sys.argv) < 3 or sys.argv[2] == "1" else run(1)