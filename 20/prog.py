import sys
import time
import re
import copy
import math
import itertools

def rotate(tile, rotation, flip):
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
    return True
#    #right
#    elif edge == 2:
#        for y in range(wh):
#            if tile1[-1][x] != tile2[0][x]:
#                return False
verb = 0
def ptile(tile, name="Tile"):
    global verb
    if not verb:
        return
    print ("Tile: ", name)
    wh=len(tile)
    for y in range(wh):
        for x in range(wh):
            print(tile[y][x], end='')
        print()

def try_place(image, x, y, keys, imap):
    if x == 0 and y == 0:
        assert(False)
    else:
        for k in keys:
            if x == 0:
#                print ("LEFT?", x, y, image[y-1][0])
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
                            print ("Match!")
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
                            print ("Match!")
                            return (k, r, f)
            else:
                (uid, urot, uflip) = image[y-1][x]
                assert(uid != 0)
                upper = imap[uid]
 #               print ("upper idx", uid, urot, uflip)
                upper = rotate(upper, urot, uflip)
                (lid, lrot, lflip) = image[y][x-1]
                assert(lid != 0)
 #               print ("left idx", lid, lrot, lflip)
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
                            print ("Match!")
                            return (k, r, f)
    return (0, 0)


def part1(imap):
    wh = int(math.sqrt(len(imap)))
    placement = None
    answch = 0
    placements = []
    for k in imap:
        for f, r, in itertools.product((0, 1, 2), (0, 90, 180, 270)):
            image = [[0 for x in range(wh)] for y in range(wh)] 
            placed = 1
            trykeys = list(imap.keys())
#                print("keys", trykeys)
            trykeys.remove(k)
#                print("keys2", trykeys)
            image[0][0] = (k, r, f)
            print ("PLACED", 0, 0, image[0][0], placed)
            print ("IMAGESTART", image)
            for y, x in itertools.product(range(wh), range(wh)):
                if x == 0 and y == 0:
                    continue
                else:
                    kk = try_place(image, x, y, trykeys, imap)
                    if kk[0] > 0:
                        print ("PLACED", x, y, kk, placed)
                        image[y][x] = kk
                        trykeys.remove(kk[0])
                        placed += 1
                        if placed == len(imap):
                            placement = image
                            placements.append(image)
                            answ = placement[0][0][0] * placement[wh-1][0][0] * placement[0][wh-1][0] * placement[wh-1][wh-1][0]
                            print ("ALL!", answ, placement)
                            if answch:
                                if answ != answch:
                                    print ("ALL NOMATCH", answ, answch)
                                asnwch = answ
                            break
                    else:
                        print ("nomatch", x, y, kk)
                        break
            
            print ("IMAGE", x, y , image)

    print ("PLACEMENTS", placements)
    if placement:
        print ("Result", placement)
        answ = placement[0][0][0] * placement[wh-1][0][0] * placement[0][wh-1][0] * placement[wh-1][wh-1][0]
        print("Answer", answ)
        for y in range(wh):
            for x in range(wh):
                print("place", x, y, placement[y][x])
    else:
        print("ERROR")
    return placements

def assemble(imap, orient):
    whimap = int(math.sqrt(len(imap)))
    whsmall = len(next(iter(imap.values())))
    whsmall1 = whsmall-2
    whbig = whimap * whsmall1
    print (whimap, whsmall, whbig)
    big = [['.' for x in range(whbig)] for y in range(whbig)] 
    for y in range(whimap):
        for x in range(whimap):
            tileo = orient[y][x]
#            print ("o", x, y, tileo)
            small = rotate(imap[tileo[0]], tileo[1], tileo[2])
#            ptile(small, "sm {0}".format(tileo))
            for yy in range(whsmall1):
                for xx in range(whsmall1):
                    big[y * whsmall1 + yy][x * whsmall1 + xx] = small[yy+1][xx+1]
    big = rotate(big, 0, 1)#why?
    ptile(big, "big!")
    return big


def check_monster(big, x, y, mon, write):
    mw = len(mon[0])
    mh = len(mon)
    if len(big) < mh + y:
#        print ("ERR1", mh, y, len(big))
        return False
    if len(big[0]) < mw + x:
#        print ("ERR2", mh, x, len(big[0]))
        return False
    for yy, xx in itertools.product(range(mh), range(mw)):
        if write:
            if mon[yy][xx] == '#':
                big[y + yy][x + xx] = "O"
#        print("monster?", x, y, xx, yy, mon[yy][xx], "b", big[y + yy][x + xx])
        if mon[yy][xx] == '#' and big[y + yy][x + xx] == '.':
#            print("no monster", xx, yy)
            return False
#        else:
#            print ("ok", y + yy, x + xx, big[y + yy][x + xx], mon[yy][xx])

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
                    print ("FOUND", f, r, x, y)

        ptile(big, "after")
        count = 0
        for x, y, in itertools.product(range(bigwh), range(bigwh)):
            if big[y][x] == "#":
                count += 1
        print ("answer", count)
        if answch != 0:
            if count != answch:
                print("answer differ", answch, count)
        answch = count

def execute(file, partnr):
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
        print("title", t, m.group(1))
        grid = [list(row) for row in rows]; w=len(grid[0]); h=len(grid)
#        ptile(grid)
        imap[idx] = grid

    print("ntiles", len(imap))

    if partnr == 0:
        orients = part1(imap)
        part2(imap, orients)
    elif partnr == 1:
        part1(imap)
    else:
        orients = [] # hardcode from part1 stdout
        part2(imap, orients)

f = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
p2 = 0 if len(sys.argv) < 3 else int(sys.argv[2])
execute(f, p2)