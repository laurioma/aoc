import sys
import re

def run_until_next(cache, bp, r1, r2, r3, r4, res1, res2, res3, res4, tryrobot, minute, maxlevel, level, chk):
    maxres = 0
    robots = [r1, r2, r3, r4]
    resources = [res1, res2, res3, res4]
    if maxlevel >= 0 and level > maxlevel:
        return -1

    robot_tried = False
    while minute > 0 and not robot_tried:
        chk[0] +=1
        minute -= 1
        new_robot = -1
        # always try to make geode robot asap
        for tryr in [3, tryrobot]:
            has_enough = True
            for resi in range(len(resources)-1):
                if resources[resi] < bp[tryr][resi]:
                    has_enough = False
                    break

            if has_enough:
                for resi in range(len(resources)-1):
                    resources[resi] -= bp[tryr][resi]
                new_robot = tryr

                if tryr != 3:
                    robot_tried = True
                break

        for ri, r in enumerate(robots):
            resources[ri] += r
 
        if new_robot >= 0:
            robots[new_robot]+=1

    if robot_tried:
        for r in range(3):
            key = (robots[0], robots[1], robots[2], robots[3], resources[0], resources[1], resources[2], resources[3], minute, r)
            if key in cache:
                res = cache[key]
            else:
                res = run_until_next(cache, bp, robots[0], robots[1], robots[2], robots[3], resources[0], resources[1], resources[2], resources[3], r, minute, maxlevel, level+1, chk)
                cache[key] = res

            if maxres < res:
                maxres = res
    else:
        assert(minute == 0)
        maxres = resources[3]

    return maxres

def run_simulation(bp, chk, maxlevel, time_limit):
    cache = {}
    maxres = 0
    for r in range(2): # no point to try to make obsidians in 1st round
        res = run_until_next(cache, bp, 1,0,0,0, 0,0,0,0, r, time_limit, maxlevel, 0, chk)
        if maxres < res:
            maxres = res
    return maxres


def run():
    lines = open(sys.argv[1]).read().splitlines()
    bps = []
    for l in lines:
        nrs = re.findall("(\d+)", l)
        nrsi = list(map(int, nrs))
        bps.append([[nrsi[1],0,0],  [nrsi[2],0,0], [nrsi[3], nrsi[4],0], [nrsi[5], 0, nrsi[6]]])

    res = 0
    max_level = -1
    time_limit=24
    for bpi, bp in enumerate(bps):
        chk = [0]
        maxobs = run_simulation(bp, chk, max_level, time_limit)
        print(bpi, "got max", maxobs, chk, max_level, time_limit)
        res += (bpi+1)*maxobs
    print("Part1", res, max_level)

    res = 1
    max_level=22
    time_limit=32
    for bpi, bp in enumerate(bps):
        chk = [0]
        maxobs = run_simulation(bp, chk, max_level, time_limit)
        print(bpi, "got max", maxobs, chk)

        res *= maxobs
        if bpi == 2:
            break

    print("Part2: ", res, max_level)

run()


