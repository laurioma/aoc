import sys 

def get_gal(matrix):
    gal = []
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == '#':
                gal.append([x, y])
    return gal

def expand_gal(matrix, gal, nlines):
    emptyr = []
    for y in range(len(matrix)):
        if all(g == '.' for g in matrix[y]):
            emptyr.append(y)
    emptyc = []
    for x in range(len(matrix[0])):
        if all(matrix[y][x] == '.' for y in range(len(matrix))):
            emptyc.append(x)

    for r in reversed(emptyr):
        for s in gal:
            if s[1] > r:
                s[1] += nlines
    for c in reversed(emptyc):
        for s in gal:
            if s[0] > c:
                s[0] += nlines
    return gal

def manhat(p1, p2):
    return sum(abs(a-b) for a, b in zip(p1, p2))

def sumdist(gal):
    sum = 0
    for i in range(len(gal)):
        for j in range(i+1, len(gal)):
            sum += manhat(gal[i], gal[j])
    return sum

def part1():
    matrix = open(sys.argv[1]).read().splitlines()

    gal = get_gal(matrix)
    gal = expand_gal(matrix, gal, 1)

    print('Part1', sumdist(gal))

def part2():
    matrix = open(sys.argv[1]).read().splitlines()

    gal = get_gal(matrix)
    gal = expand_gal(matrix, gal, 999999)

    print('Part2', sumdist(gal))

part1()
part2()