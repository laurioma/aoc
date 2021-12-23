import sys
from collections import defaultdict

def printm(room, bounds):
    for y in range(bounds[1]):
        for x in range(bounds[0]):
            if (x,y) in room:
                print(room[(x, y)], end='')
        print("")

AMPH_COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
AMPH_GOAL1 = {'A': [(3,3), (3,2)], 'B': [(5,3), (5,2)], 'C': [(7,3), (7,2)], 'D': [(9,3), (9,2)] }
AMPH_GOAL2 = {'A': [(3,5), (3,4), (3,3), (3,2)], 'B': [(5,5), (5,4), (5,3), (5,2)], 'C': [(7,5), (7,4), (7,3), (7,2)], 'D': [(9,5), (9,4), (9,3), (9,2)] }
HALL_FORBIDDEN = set([(3,1), (5,1), (7,1), (9,1)])

def find_path(room, src, dst, visited = None, l = 0):
    if visited == None:
        visited = set()
    moves = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    visited.add(src)
    movecoords = []
    for m in moves:
        coord = (src[0] + m[0], src[1] + m[1])
        if (coord not in visited) and coord in room and room[coord] == '.':
            movecoords.append(coord)
    
    if len(movecoords) == 0:
        return 0
    else:
        for coord in movecoords:
            if coord == dst:
                return 1
            v = visited.copy()
            pl = find_path(room, coord, dst, v, l+1)
            if pl > 0:
                return pl + 1
    return 0

def get_hallway_spots(room, roomsz):
    free = []
    for x in range(1, roomsz[0]):
        coord = (x, 1)
        if room[coord] == '.' and coord not in HALL_FORBIDDEN:
            free.append(coord)
    return free

def move(room, src, dst):
    assert(room[dst] == '.')
    room[dst] = room[src]
    room[src] = '.'

def check_finished(room, amph_goal):
    for k,v in amph_goal.items():
        for s in v:
            if room[s] != k:
                return False
    return True

def is_in_place(room, amph_goal, typ, pos):
    if pos not in amph_goal[typ]:
        return False
    # last one
    if pos == amph_goal[typ][0]:
        return True

    # amhs further in the room must be correct
    for g in amph_goal[typ]:
        if g == pos:
            break
        if room[g] != typ:
            return False

    return True

def get_way_home(room, amph_goal, amph):
    typ = amph[0]
    for g in amph_goal[typ]:
        if room[g] == '.' and is_in_place(room, amph_goal, typ, g):
            return g
    return (0,0)

def is_in_hallway(pos):
    if pos[1] == 1:
        return True
    return False

def get_stray_apmhs(room, amph_goal, rooms_only):
    ret = []
    for pos, typ in room.items():
        if typ not in amph_goal.keys():
            continue
        if is_in_place(room, amph_goal, room[pos], pos):
            continue
        if rooms_only and is_in_hallway(pos):
            continue
        ret.append([typ, pos])
    return ret

bestscore = sys.maxsize

runcnt = defaultdict(int)
iii = 0
finishcnt = 0
def run_game(room, amph_goal, roomsz, score, l = 0):
    global runcnt, iii, bestscore, finishcnt
    runcnt[l] += 1
    iii+=1

    # if iii % 10000 == 0:
    #     print("run_game", l, finishcnt, score, bestscore, runcnt)
    #     printm(room, roomsz)

    # move from hallway to rooms
    while True:
        moved = False
        stray_amphs = get_stray_apmhs(room, amph_goal, False)
        for amph in stray_amphs:
            home = get_way_home(room, amph_goal, amph)
            if home != (0,0):
                pathl = find_path(room, amph[1], home)
                if pathl > 0:
                    moved = True
                    # print("move to room", l, amph, good)
                    move(room, amph[1], home)
                    # printm(room, roomsz)
                    movecost = pathl * AMPH_COST[amph[0]]
                    score = score + movecost
                    if check_finished(room, amph_goal):
                        # print("Finished", score, bestscore)
                        # printm(room, roomsz)
                        finishcnt+=1
                        if bestscore > score:
                            bestscore = score
                        return
        if not moved:
            # print("did no good")
            break

    # move from rooms to hallway
    free_hw = get_hallway_spots(room, roomsz)
    room_amphs = get_stray_apmhs(room, amph_goal, True)
    for amph in room_amphs:
        for spot in free_hw:
            # print("check", l, amph, spot)
            pathl = find_path(room, amph[1], spot)
            if pathl > 0:
                movecost = pathl * AMPH_COST[amph[0]]
                nscore = score + movecost

                if nscore > bestscore:
                    continue

                nroom = room.copy()
                # print("move out", l, amph, spot)
                move(nroom, amph[1], spot)
                # printm(nroom, roomsz)

                run_game(nroom, amph_goal, roomsz, nscore, l+1)

def run(part2):
    lines = open(sys.argv[1]).read().splitlines()
    if part2:
        lines.insert(3, "  #D#B#A#C#")
        lines.insert(3, "  #D#C#B#A#")

    x = 0
    y = 0
    room = {}
    amphs = []
    for l in lines:
        for x, c in enumerate(l):
            room[(x, y)] = c
            if c in AMPH_COST.keys():
                amphs.append([c, (x, y)]) # type, coord
        y+=1
    roomsz = (len(lines[0]),y)
    printm(room, roomsz)
    goal = AMPH_GOAL2 if part2 else AMPH_GOAL1
    run_game(room, goal, roomsz, 0)
    print("Part", 2 if part2 else 1, bestscore)

run(0) if len(sys.argv) < 3 or sys.argv[2] == "1" else run(1)