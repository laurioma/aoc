
import sys
import itertools
import re

MAX_ORJENTATIONS=48

def get_orientation(pos, i):
    x = pos[0] * (-1 if i & 1 else 1)
    y = pos[1] * (-1 if i & 2 else 1)
    z = pos[2] * (-1 if i & 4 else 1)
    if i < 8:
        return (x, y, z)
    elif i < 16:
        return (x, z, y)
    elif i < 24:
        return (y, x, z)
    elif i < 32:
        return (y, z, x)
    elif i < 40:
        return (z, x, y)
    else:
        return (z, y, x)

def equal_points(o1, o2):
    return o1[0].intersection(o2[0])

def resolve_scanner_pos(scanners, s1, s2, s1rel, s2rel, s1orj, s2orj):
    s1i = s1rel.index((0,0,0))
    s2i = s2rel.index((0,0,0))
    s1point = scanners[s1][0][s1i]
    s2point = scanners[s2][0][s2i]
#    print("resolve", s1point, s2point)
    s1point_corrected = get_orientation(s1point, s1orj)
    s2point_corrected = get_orientation(s2point, s2orj)
#    print("resolvecorr", s1point_corrected, s2point_corrected)
    s2relpos = (s1point_corrected[0] - s2point_corrected[0], s1point_corrected[1] - s2point_corrected[1], s1point_corrected[2] - s2point_corrected[2])
    assert scanners[s1][1] != (-1,-1,-1)
    s1pos = scanners[s1][1]
    abspos = (s2relpos[0] + s1pos[0], s2relpos[1] + s1pos[1], s2relpos[2] + s1pos[2])
    return abspos

def run():
    lines = open(sys.argv[1]).read().splitlines()
    scannerid = 0
    scanners = {}
    for l in lines:
        m = re.search("scanner (\d+)", l)
        if m:
            scannerid = int(m.group(1))
            if scannerid == 0:
                scanners[scannerid] = [[], (0,0,0), 0] #points, pos, orj
            else:
                scanners[scannerid] = [[], (-1,-1,-1), -1] #points, pos, orj
        elif len(l) > 1:
            a = [int(n) for n in l.split(",")]
            scanners[scannerid][0].append((a[0], a[1], a[2]))

    # for each scanner find all translations where one point is taken as an origin instead of scanner. then calculate all possible orientations for each translation
    translations = {}
    for s in scanners:
        translations[s] = {}
        for i in range(len(scanners[s][0])):
            zero = scanners[s][0][i]
            translations[s][i] = {}
            for o in range(MAX_ORJENTATIONS):
                translations[s][i][o] = (set(), [])
            for j in range(len(scanners[s][0])):
                translated = (scanners[s][0][j][0] - zero[0], scanners[s][0][j][1] - zero[1], scanners[s][0][j][2] - zero[2])
                for o in range(MAX_ORJENTATIONS):
                    translations[s][i][o][0].add(get_orientation(translated, o))
                    translations[s][i][o][1].append(get_orientation(translated, o))

    resolved_scanners = [0]
    unresolved_scanners = list(scanners.keys())
    unresolved_scanners.remove(0)
    # compare all the translations and orientations of each scanner
    while len(unresolved_scanners):
        resolved = []
        for i, j in itertools.product(resolved_scanners, unresolved_scanners):
            if j in resolved:
                continue
            found = False
            for s1t, s2t in itertools.product(range(len(translations[i])), range(len(translations[j]))):
                for o in range(MAX_ORJENTATIONS):
                    assert scanners[i][1] != (-1,-1,-1)
                    eq = equal_points(translations[i][s1t][scanners[i][2]], translations[j][s2t][o])
                    if len(eq) >= 12:
                        res = resolve_scanner_pos(scanners, i, j, translations[i][s1t][0][1], translations[j][s2t][0][1], scanners[i][2], o)
#                        print("scanner", i, j, "trans", s1t, s2t, "orj", scanners[i][2], o, "res", res)
                        scanners[j][1] = res
                        scanners[j][2] = o
                        resolved.append(j)
                        found = True
                        break
                if found:
                    break
        
        if len(resolved) == 0:
            print("Failed to resolve all scanners!")
            break
        else:
            resolved_scanners = resolved
            for r in resolved:
                unresolved_scanners.remove(r)
#        print("res", resolved_scanners, "unres", unresolved_scanners)

    s1_points = set()
    for s in scanners:
        for p in scanners[s][0]:
            if scanners[s][1] == (0,0,0):
                s1_points.add(p)
            else:
                spos = scanners[s][1]
                relpos = get_orientation(p, scanners[s][2])
                pos = (spos[0] + relpos[0], spos[1] + relpos[1], spos[2] + relpos[2])
#                print("scanner", s, scanners[s][2], "spos", scanners[s][1],"spos1", spos, "orig", p, "orient", relpos, "res", pos)
                s1_points.add(pos)
    print("Part1", len(s1_points))

    largestdist = 0
    for i, j in itertools.combinations(range(len(scanners)), 2):
        mdist = abs(scanners[i][1][0] - scanners[j][1][0]) +  abs(scanners[i][1][1] - scanners[j][1][1]) + abs(scanners[i][1][2] - scanners[j][1][2])
        if mdist > largestdist:
            largestdist = mdist
        
    print("Part2", largestdist)


run()
