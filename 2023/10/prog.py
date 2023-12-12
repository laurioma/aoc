import sys
import itertools

def printm(matrix, path = {}):
    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            k = (c, r)
            if k in path:
                print(path[k], end='')
            else:
                print(matrix[r][c], end='')
        print("")

def find(map, sym):
    for y, x in itertools.product(range(len(map)), range(len(map[0]))): 
        if map[y][x] == sym:
            return x,y

def move(map):
    steps = 0
    x, y = find(map, 'S')
    #print('start', x, y, map[y][x])
    path = {}
    while True:
#        print(x,y, map[y][x])
        steps+=1
        if map[y][x] in ['S', '-', 'J', '7'] and x-1 >= 0 and (x-1, y) not in path and map[y][x-1] in ['-', 'L', 'F']:
            path[(x,y)] = 'l'
            x -= 1
        elif map[y][x] in ['S', '|', '7', 'F'] and y+1 < len(map) and (x, y+1) not in path and map[y+1][x] in ['|', 'L', 'J']:
            path[(x,y)] = 'd'
            y += 1
        elif map[y][x] in ['S', '-', 'F', 'L'] and x+1 < len(map[y]) and (x+1, y) not in path and map[y][x+1] in ['-', '7', 'J']:
            path[(x,y)] = 'r'
            x += 1
        elif map[y][x] in ['S', '|', 'L', 'J'] and y-1 >= 0 and (x, y-1) not in path and map[y-1][x] in ['|', '7', 'F']:
            path[(x,y)] = 'u'
            y -= 1
        else:
            path[(x,y)] = 'x'
#            print('stop', x, y, map[y][x], steps)
            break
    assert len(path) == steps
    return path

LEFT = '1'
RIGHT = '2'

def wr_edge(map, x, y, ech):
    if y >= 0 and x >= 0 and y < len(map) and x < len(map[0]) and map[y][x] == '.':
        map[y][x] = ech

def mark_edges(map, path):
    for (x,y) in path.keys():
        dir = path[(x,y)]
        if dir == 'x':
            continue
        if map[y][x] == '|':
            assert dir == 'u' or dir == 'd', '|'
            wr_edge(map, x-1, y, LEFT if dir == 'u' else RIGHT)
            wr_edge(map, x+1, y, RIGHT if dir == 'u' else LEFT)
        elif map[y][x] == '-':
            assert dir == 'l' or dir == 'r', '-'
            wr_edge(map, x, y+1, LEFT if dir == 'l' else RIGHT)
            wr_edge(map, x, y-1, RIGHT if dir == 'l' else LEFT)
        elif map[y][x] == 'L':
            assert dir == 'u' or dir == 'r', 'L'
            for (xx, yy) in [(x, y+1), (x-1, y+1), (x-1, y)]:
                wr_edge(map, xx, yy, LEFT if dir == 'u' else RIGHT)
        elif map[y][x] == 'J':
            assert dir == 'u' or dir == 'l', 'J'
            for (xx, yy) in [(x, y+1), (x+1, y+1), (x+1, y)]:
                wr_edge(map, xx, yy, LEFT if dir == 'l' else RIGHT)
        elif map[y][x] == '7':
            assert dir == 'l' or dir == 'd', '7'
            for (xx, yy) in [(x+1, y), (x+1, y-1), (x, y-1)]:
                wr_edge(map, xx, yy, LEFT if dir == 'd' else RIGHT)
        elif map[y][x] == 'F':
            assert dir == 'd' or dir == 'r', 'F'
            for (xx, yy) in [(x, y-1), (x-1, y-1), (x-1, y)]:
                wr_edge(map, xx, yy, LEFT if dir == 'r' else RIGHT)         

def expand(map, char):
    while True:
        cnt = 0
        for y, x in itertools.product(range(len(map)), range(len(map[0]))): 
            if map[y][x] == char:
                for dy, dx in itertools.product([-1, 1], [-1, 1]): 
                    nx = x + dx
                    ny = y + dy
                    if nx >= 0 and nx < len(map[0]) and ny >= 0 and ny < len(map) and map[ny][nx] == '.':
                        map[ny][nx] = char
                        cnt += 1
        if cnt == 0:
            break

def count(map, char):
    count = 0
    for y, x in itertools.product(range(len(map)), range(len(map[0]))): 
        if map[y][x] == char:
            count += 1
    return count

def part1():
    map = open(sys.argv[1]).read().splitlines()
    #printm(map)
    path = move(map)
    print('Part1', len(path)//2)

def part2():
    lines = open(sys.argv[1]).read().splitlines()
    map = [list(row) for row in lines]

    # clean junk
    path = move(map)
    for y, x in itertools.product(range(len(map)), range(len(map[0]))): 
        if (x, y) not in path:
            map[y][x] = '.'

    mark_edges(map, path)
    #printm(map, path) 

    expand(map, '1')
    expand(map, '2')
    in_char = '2' if map[0][0] == '1' else '1'
    print('Part2', count(map, in_char))

part1()
part2()