import sys
import time
import re
import copy
import math
import itertools
import numpy as np

def vprint(*args, end='\n'):
    verb = 0
    if verb:
        print(*args, end=end)

def ptile(tile, name="Tile"):
    vprint("Tile: ", name)
    wh=len(tile)
    for y in range(wh):
        for x in range(wh):
            vprint(tile[y][x], end='')
        vprint()

def rotate_std(tile, rotation, flip):
    wh=len(tile)
    flipt = []
    if flip == 0:
        flipt = tile
    elif flip == 1:
        for y in range(wh):
            newr = []
            for x in range(wh):
                newr.append(tile[y][wh - 1 - x])
            flipt.append(newr)
    elif flip == 2:
        for y in range(wh):
            newr = []
            for x in range(wh):
                newr.append(tile[wh - y - 1][x])
            flipt.append(newr)

    rott = []
    if rotation == 0:
        return flipt
    if rotation == 90:
        for y in range(wh):
            newr = []
            for x in range(wh):
                newr.append(flipt[wh -1 - x][y])
            rott.append(newr)
    if rotation == 180:
        for y in range(wh):
            newr = []
            for x in range(wh):
                newr.append(flipt[y][wh -1 - x])
            rott.insert(0, newr)
    if rotation == 270:
        for y in range(wh):
            newr = []
            for x in range(wh):
                newr.append(flipt[x][y])
            rott.insert(0, newr)
    return rott

def rotate_np(tile, rotation, flip):
    ret = tile
    if flip == 0:
        pass
    elif flip == 1:
        ret = np.flip(tile, 1)
    elif flip == 2:
        ret = np.flip(tile, 0)
    else:
        assert(), "invalid flip %d" % flip

    if rotation == 0:
        pass
    elif rotation == 90:
        ret = np.rot90(ret, 3)
    elif rotation == 180:
        ret = np.rot90(ret, 2)
    elif rotation == 270:
        ret = np.rot90(ret, 1)
    else:
        assert(), "invalid rot %d" % rotation

    return ret

def rotate(tile, rotation, flip):
    global nump
    if nump:
        return rotate_np(tile, rotation, flip)
    else:
        return rotate_std(tile, rotation, flip)

def edge_matches(tile1, tile2, edge):
    wh=len(tile1)

    # left
    if edge == 0:
        for y in range(wh):
            if tile1[y][-1] != tile2[y][0]:
                return False
    #bottom
    elif edge == 1:
        for x in range(wh):
            if tile1[-1][x] != tile2[0][x]:
                return False
    else:
        assert(False), edge
    return True


def try_place(image, x, y, keys, imap):
    if x == 0 and y == 0:
        assert(False)
    else:
        for k in keys:
            if x == 0:
                (uid, urot, uflip) = image[y-1][0]
                assert(uid != 0)
                upper = imap[uid]
                upper = rotate(upper, urot, uflip)
                ptile(upper, "upper" + str(uid) + str(urot))
                for f in (0, 1, 2):
                    for r in (0, 90, 180, 270):
                        place = imap[k].copy()
                        if r != 0:
                            place = rotate(place, r, f)
                        ptile(place, "place {0} {1} {2}".format(k, r, f))
                        if edge_matches(upper, place, 1):
                            vprint ("try_place match")
                            return (k, r, f)
            elif y == 0:
                (lid, lrot, lflip) = image[0][x-1]
                assert(lid != 0)
                left = imap[lid]
                left = rotate(left, lrot, lflip)
                ptile(left, "left")
                for f in (0, 1, 2):
                    for r in (0, 90, 180, 270):
                        place = imap[k].copy()
                        if r != 0:
                            place = rotate(place, r, f)
                        ptile(place, "place {0} {1} {2}".format(k, r, f))
                        if edge_matches(left, place, 0):
                            vprint ("try_place match")
                            return (k, r, f)
            else:
                (uid, urot, uflip) = image[y-1][x]
                assert(uid != 0)
                upper = imap[uid]
                upper = rotate(upper, urot, uflip)
                (lid, lrot, lflip) = image[y][x-1]
                assert(lid != 0)
                left = imap[lid]
                left = rotate(left, lrot, lflip)
                ptile(upper, "upper")
                ptile(left, "left")
                for f in (0, 1, 2):
                    for r in (0, 90, 180, 270):
                        place = imap[k].copy()
                        if r != 0:
                            place = rotate(place, r, f)
                        ptile(place, "place {0} {1} {2}".format(k, r, f))
                        if edge_matches(upper, place, 1) and edge_matches(left, place, 0):
                            vprint ("try_place match")
                            return (k, r, f)
    return (0, 0)

def part1(imap, max_placements):
    wh = int(math.sqrt(len(imap)))
    placement = None
    answch = 0
    placements = []
    for k, f, r, in itertools.product(imap, (0, 1, 2), (0, 90, 180, 270)):
        image = [[0 for x in range(wh)] for y in range(wh)] 
        placed = 1
        trykeys = list(imap.keys())
        trykeys.remove(k)
        image[0][0] = (k, r, f)
        vprint("Start image", image)
        for y, x in itertools.product(range(wh), range(wh)):
            if x == 0 and y == 0:
                continue
            else:
                kk = try_place(image, x, y, trykeys, imap)
                if kk[0] > 0:
                    vprint ("PLACED", x, y, kk, placed)
                    image[y][x] = kk
                    trykeys.remove(kk[0])
                    placed += 1
                    if placed == len(imap):
                        placement = image
                        placements.append(image)
                        answ = placement[0][0][0] * placement[wh-1][0][0] * placement[0][wh-1][0] * placement[wh-1][wh-1][0]
                        print("ALL PLACED", answ, placement)
                        if answch:
                            if answ != answch:
                                print ("ALL Different answers!!", answ, answch)
                            asnwch = answ
                        break
                else:
                    vprint("nomatch", x, y, kk)
                    break
        if len(placements) >= max_placements:
            print("got enough placements")
            break

    print ("PLACEMENTS", placements)
    if placement:
        answ = placement[0][0][0] * placement[wh-1][0][0] * placement[0][wh-1][0] * placement[wh-1][wh-1][0]
        print("Answer1", answ)
    else:
        print("PLACEMENT ERROR")
    return placements

def assemble(imap, orient):
    whimap = int(math.sqrt(len(imap)))
    whsmall = len(next(iter(imap.values())))
    whsmall1 = whsmall-2
    whbig = whimap * whsmall1
    big = [['.' for x in range(whbig)] for y in range(whbig)] 
    for y in range(whimap):
        for x in range(whimap):
            tileo = orient[y][x]
            small = rotate(imap[tileo[0]], tileo[1], tileo[2])
            for yy in range(whsmall1):
                for xx in range(whsmall1):
                    big[y * whsmall1 + yy][x * whsmall1 + xx] = small[yy+1][xx+1]
    big = rotate(big, 0, 1) #match assignment example
    ptile(big, "big!")
    return big


def check_monster(big, x, y, mon, write):
    mw = len(mon[0])
    mh = len(mon)
    if len(big) < mh + y:
        return False
    if len(big[0]) < mw + x:
        return False
    for yy, xx in itertools.product(range(mh), range(mw)):
        if write:
            if mon[yy][xx] == '#':
                big[y + yy][x + xx] = "O"
        if mon[yy][xx] == '#' and big[y + yy][x + xx] == '.':
            return False

    return True

def part2(imap, orients):
    monss = \
"""                  #   
#    ##    ##    ###  
 #  #  #  #  #  #     """
    mon = []
    monss2 = monss.split("\n")
    for y in range(3):
        monr = []
        for x in range(20):
            monr.append(monss2[y][x])
        mon.append(monr)
    #print(mon)

    answch = 0
    for orient in orients:
        big = assemble(imap, orient)
        bigwh = len(big)

        ptile(big, "withmonster")
        for f, r, in itertools.product((0, 1, 2), (0, 90, 180, 270)):
            big = rotate(big, r, f)
            for x, y, in itertools.product(range(bigwh), range(bigwh)):
                if check_monster(big, x, y, mon, 0):
                    check_monster(big, x, y, mon, 1)
                    vprint("FOUND", f, r, x, y)

        ptile(big, "after")
        count = 0
        for x, y, in itertools.product(range(bigwh), range(bigwh)):
            if big[y][x] == "#":
                count += 1
        print("Answer2", count)
        if answch != 0:
            if count != answch:
                print("Answer2 differ", answch, count)
        answch = count

def execute(file, partnr):
    global nump
    data = ""
    with open(file) as f:
        data = f.read()

    imap = {}
    idx = 0
    imgtxt = data.split('\n\n')
    for img in imgtxt:
        rows = img.split('\n')
        t = rows.pop(0)
        m = re.search("Tile (\d+)", t)
        idx = int(m.group(1))
        vprint("title", t, m.group(1))
        grid = [list(row) for row in rows]; w=len(grid[0]); h=len(grid)
        ptile(grid)
        if nump:
            gridn = np.array(grid)
            imap[idx] = gridn
        else:
            imap[idx] = grid

    # seems the images can be assembled in multiple (2) ways
    max_placements = 2

    if partnr == 0:
        orients = part1(imap, max_placements)
        part2(imap, orients)
    elif partnr == 1:
        part1(imap, max_placements)
    else:
        orients = [] # hardcode from part1 stdout
        part2(imap, orients)

f = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
p2 = 0 if len(sys.argv) < 3 else int(sys.argv[2])
nump = 0 if len(sys.argv) < 4 else int(sys.argv[3])

if (nump):
    print ("Numpy!")

execute(f, p2)