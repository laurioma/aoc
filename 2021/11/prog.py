import sys 

def printm(matrix):
    for r in matrix:
        for c in r:
            print("%1d" % int(c), end='')
        print("")

def step(grid, w, h):
    for y in range(h):
        for x in range(w):
            grid[y][x] += 1

def flash(grid, w, h, flashed):
    someflashed = False
    for y in range(h):
        for x in range(w):
            if grid[y][x] > 9 and (x, y) not in flashed:
                flashed.append((x, y))
                for yy in (y - 1, y, y+1):
                    for xx in (x - 1, x, x+1):
                        if xx >= 0 and xx < w and yy >= 0 and yy < h:
                            grid[yy][xx] += 1
                            someflashed = True
    return someflashed



def run(part2):
    lines = open(sys.argv[1]).read().splitlines()
    grid = [[int(c) for c in row] for row in lines]; w=len(grid[0]); h=len(grid)

    countf = 0
    max = 100 if not part2 else 10000
    answ = 0
    for s in range(max):
        flashed = []
        step(grid, w, h)
        while flash(grid, w, h, flashed):
            #printm(grid)
            continue
        countf += len(flashed)
        if len(flashed) == 100:
            #print ("allflashed!!")
            answ = s+1
            break
        for y in range(h):
            for x in range(w):
                if grid[y][x] > 9:
                    grid[y][x] = 0
        print("step", s+1, countf)
        answ = countf
        #printm(grid)
    print("Part", 2 if part2 else 1, answ)



run(0) if len(sys.argv) < 3 or sys.argv[2] == "1" else run(1)

