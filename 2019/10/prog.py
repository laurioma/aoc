
import sys
import copy
import math

def printm(grid, dim):
    for y in range(dim[1]):
        for x in range(dim[0]):
            c = grid[(x, y)] if (x, y) in grid else 0
            print(" {0:+06.2F}".format(float(c)), end='')
        print("")

def get_best_asteroid(grid, dim):
    for c in grid:
        testset = set()
        for cc in grid:
            if c == cc:
                continue
            dx = c[0]-cc[0]
            dy = c[1]-cc[1]
            k = math.atan2(dx, dy)
            if k in testset:
                continue
            testset.add(k)
            grid[c] += 1
    # printm(grid, dim)
    best = max(grid, key=grid.get)
    return grid[best], best

def spin_laser(grid, lpos, dim, target_cnt):
    destroy_cnt = 0

    while True:
        destroy_order = []
        for c in grid:
            if c in grid and c != lpos:
                dx = lpos[0]-c[0]
                dy = lpos[1]-c[1]
                k = math.atan2(-dx, -dy)
                dst = dy * dy + dx * dx
                destroy_order.append((k, -dst, c))
        destroy_order.sort(reverse=True)

        last_k = -10
        destroyed = False
        for do in destroy_order:
            # blocked
            if do[0] == last_k:
                continue
            last_k = do[0]
            destroyed = True
            destroy_cnt+=1
            del grid[do[2]]
            if destroy_cnt == target_cnt:
                return True, do[2]
        if not destroyed:
            break

    return False, (0,0)

def run():
    lines = open(sys.argv[1]).read().splitlines()
    grid = {(x,y):1 for y in range(len(lines)) for x in range(len(lines[0])) if lines[y][x] != '.'}
    dim = (len(lines[0]), len(lines))
    best, bestc = get_best_asteroid(grid, dim)
    print("Part1", best, bestc)
    ret, dst = spin_laser(grid, bestc, dim, 200)
    assert(ret)
    print("Part2", dst[0]*100+dst[1])



run()