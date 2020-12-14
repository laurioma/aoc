import sys

floor0 = []

with open(sys.argv[1]) as f:
    for line in f:
        floor0.append(line.rstrip())

def count_adjecent(floor, x, y, state):
    count = 0
    for yy in range (y-1, y+2):
        for xx in range (x-1, x+2):
            if (xx < 0 or xx >= len(floor[0]) or yy < 0 or yy >= len(floor) or (xx == x and yy == y)):
                continue
            else:
                if floor[yy][xx] == state:
                    count += 1
    return count

def count_direction(floor, x, y, state, direction):
    xx = x
    yy = y
    while (True):
        if direction == 0:
            xx -= 1
        elif direction == 1:
            xx -= 1
            yy -= 1
        elif direction == 2:
            yy -= 1
        elif direction == 3:
            xx += 1
            yy -= 1
        elif direction == 4:
            xx += 1
        elif direction == 5:
            xx += 1
            yy += 1
        elif direction == 6:
            yy += 1
        elif direction == 7:
            xx -= 1
            yy += 1
        if (xx < 0 or yy < 0 or xx >= len(floor[0]) or yy >= len(floor)):
            break
        inv_state = 'L' if state == '#' else '#'
#        if (x == 3 and y == 0):
#            print ("count d ", direction, "xy", x, y, " xx yy", xx, yy, "s", state, inv_state, "F ", floor[yy][xx])
        if (floor[yy][xx] == state):
            return 1
        if floor[yy][xx] == inv_state:
            return 0 
    return 0


def count_8_directions(floor, x, y, state):
    count = 0
    for d in range(8):
        count += count_direction(floor, x, y, state, d)
#    if (x == 3 and y == 0):
#        print ("count8 xy ", x, y, count)
    return count


def add_people(floor, part2):
    new_floor = []
    for y in range(len(floor)):
        new_row = []
        for x in range(len(floor[y])):
            if part2:
                if floor[y][x] == "L" and count_8_directions(floor, x, y, "#") == 0:
                    new_row.append("#")
                else:
                    new_row.append(floor[y][x])
            else:
                if floor[y][x] == "L" and count_adjecent(floor, x, y, "#") == 0:
                    new_row.append("#")
                else:
                    new_row.append(floor[y][x])
        new_floor.append(new_row)
    return new_floor

def remove_people(floor, part2):
    new_floor = []
    for y in range(len(floor)):
        new_row = []
        for x in range(len(floor[y])):
            if part2:
                if floor[y][x] == "#" and count_8_directions(floor, x, y, "#") >= 5:
                    new_row.append("L")
                else:
                    new_row.append(floor[y][x])
            else:
                if floor[y][x] == "#" and count_adjecent(floor, x, y, "#") >= 4:
                    new_row.append("L")
                else:
                    new_row.append(floor[y][x])
        new_floor.append(new_row)
    return new_floor

def count_occup(floor):
    count = 0
    for y in range(len(floor)):
        for x in range(len(floor[y])):
            if floor[y][x] == "#":
                count += 1
    return count


def printfloor(floor, name):
    print("floor ", name)
    for y in range(len(floor)):
        print(floor[y])

def run_simulation(part2):
    iteration = 0
    count_rem_prev = -1
    start_f = floor0
    while (True):
        floor_add = add_people(start_f, part2)
        floor_rem = remove_people(floor_add, part2)
        start_f = floor_rem
        printfloor(floor_add, "floor_add")
        printfloor(floor_rem, "floor_rem")

        count_add = count_occup(floor_add)
        count_rem = count_occup(floor_rem)
        iteration += 1
        print ("iteration ", iteration, " occup ", count_add, count_rem)

        if count_rem_prev == count_rem:
            break
        count_rem_prev = count_rem


run_simulation(int(sys.argv[2]))