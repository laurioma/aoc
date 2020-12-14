import sys

facing = 90
x = 0
y = 0
wpt_x = 10
wpt_y = 1

def move_ship(cmd, unit):
    global x, y, facing
    if cmd == 'N':
        y += unit 
    elif cmd == 'S':
        y -= unit 
    elif cmd == 'E':
        x += unit 
    elif cmd == 'W':
        x -= unit 
    elif cmd == 'L':
        facing = (facing - unit) % 360
    elif cmd == 'R':
        facing = (facing + unit) % 360
    elif cmd == 'F':
        if facing == 0:
            y += unit
        elif facing == 90:
            x += unit
        elif facing == 180:
            y -= unit
        elif facing == 270:
            x -= unit
        else:
            print ("Invalid facing ", facing)
    print("x, y, f", x, y, facing)


def move_waypoint(cmd, unit):
    global wpt_x, wpt_y
    wpt_xb4 = wpt_x
    wpt_yb4 = wpt_y
    if cmd == 'N':
        wpt_y += unit 
    elif cmd == 'S':
        wpt_y -= unit 
    elif cmd == 'E':
        wpt_x += unit 
    elif cmd == 'W':
        wpt_x -= unit 
    elif cmd == 'L':
        if unit == 90:
            wpt_x = -wpt_y
            wpt_y = wpt_xb4
        elif unit == 180:
            wpt_x = -wpt_x
            wpt_y = -wpt_y
        elif unit == 270:
            wpt_x = wpt_y
            wpt_y = -wpt_xb4
    elif cmd == 'R':
        if unit == 90:
            wpt_x = wpt_y
            wpt_y = -wpt_xb4
        elif unit == 180:
            wpt_x = -wpt_x
            wpt_y = -wpt_y
        elif unit == 270:
            wpt_x = -wpt_y
            wpt_y = wpt_xb4
    print("WPT ", wpt_x, wpt_y)

def move_to_waypoint(unit):
    global x, y, wpt_x, wpt_y
    xb4 = x
    yb4 = y
    x += wpt_x * unit
    y += wpt_y * unit
    print("SHIP ", xb4, yb4, " -> ", x, y, "WPT", wpt_x, wpt_y)

def run(part2):
    with open(sys.argv[1]) as f:
        for line in f:
            cmd = line[0]
            unit = int(line[1:])
            print ("CMD", cmd, unit)
            if part2:
                if (cmd == 'F'):
                    move_to_waypoint(unit)
                else:
                    move_waypoint(cmd, unit)
            else:
                move_ship(cmd, unit)
            print ("SHIP", x, y, "MHT:", abs(x) + abs(y))
            
run(int(sys.argv[2]))
