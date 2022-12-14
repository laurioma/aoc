import sys

def printm(img, tl, br):
    for y in range(tl[1], br[1]+1):
        for x in range(tl[0], br[0]+1):
            print(img[(x,y)] if (x, y) in img else '.', end='')
        print("")

def get_bounds(matrix):
    ymin = xmin = sys.maxsize
    xmax = ymax = -sys.maxsize
    for (x,y) in matrix.keys():
        xmin = min(xmin, x)
        xmax = max(xmax, x)
        ymin = min(ymin, y)
        ymax = max(ymax, y)
    tl = (xmin, ymin)
    br = (xmax, ymax)
    return (tl, br)

def range2(start, stop):
    step = -1 if start > stop else 1
    return range(start, stop + step, step)

def drop_sand(matrix, tl, br, part):
    x = 500
    y = 0
    while True:
        y = y+1
        #floor
        if part == 2 and y == br[1]+2:
            matrix[(x,y-1)] = 'o'
            return True

        if (x,y) in matrix:
            # try left
            if (x-1,y) not in matrix:
                x -= 1
            # try right
            elif (x+1,y) not in matrix:
                x += 1
            # rest
            else:
                matrix[(x,y-1)] = 'o'
                # full
                if part == 2 and y == 1:
                    return False
                else:
                    return True
        # fell down
        if part == 1 and y > br[1]:
            return False


def run(part):
    lines = open(sys.argv[1]).read().splitlines()
    matrix = {}
    matrix[(500,0)] = '+'
    for l in lines:
        ll = l.split(' -> ')
        prev = (-1,-1)
        for lll in ll:
            p = lll.split(',')
            point = (int(p[0]), int(p[1]))

            if prev != (-1, -1):
                for x in range2(prev[0], point[0]):
                    for y in range2(prev[1], point[1]):
                        matrix[(x,y)] = '#'
            prev = point

    (tl, br) = get_bounds(matrix)
    # print(tl, br)
    # printm(matrix, tl, br)
    count = 0
    while drop_sand(matrix, tl, br, part):
        count +=1
    # (tl, br) = get_bounds(matrix)
    # printm(matrix, tl, br)
    if part == 2:
        count +=1
    print ('Part%d %d' % (part, count))

run(1)
run(2)
