import sys
import re

def run_until_next(cache, bp, robots, resources, tryrobot, minute, maxlevel, level, chk, time_limit):
    maxres = 0
    robots_diff=[0,0,0,0]
    resources_diff = [0,0,0,0]
    
    if maxlevel >= 0 and level > maxlevel:
        return -1

    robot_tried = False
    while minute < time_limit and not robot_tried:
        chk[0] +=1
        minute += 1
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
                    resources_diff[resi] -= bp[tryr][resi]
                new_robot = tryr

                if tryr != 3:
                    robot_tried = True
                break

        for ri, r in enumerate(robots):
            resources[ri] += r
            resources_diff[ri] += r
        if new_robot >= 0:
            robots_diff[new_robot]+=1
            robots[new_robot]+=1

    if robot_tried:
        for r in range(3):
            key = (robots[0], robots[1], robots[2], robots[3], resources[0], resources[1], resources[2], resources[3], minute, r)
            if key in cache:
                res = cache[key]
            else:
                res = run_until_next(cache, bp, robots, resources, r, minute, maxlevel, level+1, chk, time_limit)
                cache[key] = res

            if maxres < res:
                maxres = res
    else:
        assert(minute == time_limit)
        maxres = resources[3]

    for i in range(4):
        robots[i] -= robots_diff[i]
        assert(robots[i] >= 0)
        resources[i] -= resources_diff[i]
        assert(resources[i] >= 0)
    return maxres

def run_simulation(bp, chk, maxlevel, time_limit):
    cache = {}
    maxres = 0
    robots=[1,0,0,0]
    resources = [0,0,0,0]
    for r in range(2): # no point to try to make obsidians in 1st round
        res = run_until_next(cache, bp, robots, resources, r, 0, maxlevel, 0, chk, time_limit)
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


