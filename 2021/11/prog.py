import sys 
import itertools

def printm(matrix):
    for r in matrix:
        for c in r:
            print("%1d" % int(c), end='')
        print("")

def flash(grid, w, h, x, y):
    flashcnt = 1
    for yy, xx in itertools.product((y - 1, y, y+1), (x - 1, x, x+1)):
        if xx >= 0 and xx < w and yy >= 0 and yy < h:
            grid[yy][xx] += 1
            if grid[yy][xx] == 10:
                flashcnt += flash(grid, w, h, xx, yy)

    return flashcnt

def run(part2):
    lines = open(sys.argv[1]).read().splitlines()
    grid = [[int(c) for c in row] for row in lines]; w=len(grid[0]); h=len(grid)

    max = 100 if not part2 else sys.maxsize
    totalfcnt = 0
    goal_fcnt = w*h
    for s in range(max):
        flashcnt = 0
        # everyone +1
        for y, x in itertools.product(range(h), range(w)): 
            grid[y][x] += 1
            # run the flashing 
            if grid[y][x] == 10:
                flashcnt += flash(grid, w, h, x, y)

        # flip to 0
        for y, x in itertools.product(range(h), range(w)):
            if grid[y][x] > 9:
                grid[y][x] = 0

        totalfcnt += flashcnt
        #print ("step", s+1, "flashcnt", flashcnt, "total", totalfcnt)
        #printm(grid)
        if part2:
            if flashcnt == goal_fcnt:
                print("Part2", s+1)
                break
    if not part2:
        print("Part1", totalfcnt)



run(0) if len(sys.argv) < 3 or sys.argv[2] == "1" else run(1)

