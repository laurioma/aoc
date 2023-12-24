import sys
from sympy import symbols, Eq, solve

def parse():
    lines = open(sys.argv[1]).read().splitlines()
    stones = []
    for l in lines:
        ll = l.split('@')
        p = [int(s) for s in ll[0].split(', ')]
        d = [int(s) for s in ll[1].split(', ')]
        stones.append((p, d))
    return stones

# solve system of equations x1 + dx1*t1 = x2 + dx2*t2, y1 + dy1*t1 = y2 + dy2*t2 manually
def intersect_xy(l1, l2, rmin, rmax):
    ((x1, y1, _), (dx1, dy1, _)) = l1
    ((x2, y2, _), (dx2, dy2, _)) = l2
     
    div = dx1 * dy2 - dy1 * dx2
    if div == 0:
        return False 
    
    t1 = (dx2*y1-dx2*y2-dy2*x1+dy2*x2)/div
    t2 = (dx1*y1-dx1*y2-dy1*x1+dy1*x2)/div
    xx = x1 + t1 * dx1
    yy = y1 + t1 * dy1
    if t1 >= 0 and t2 >= 0 and rmin <= xx <= rmax and rmin <= yy <= rmax:
        return True
    return False


def part1():
    stones = parse()
    cnt = 0
    rmin, rmax = (7, 27) if sys.argv[1] == "test.txt" else (200000000000000, 400000000000000)
    for i, s1 in enumerate(stones):
        for j in range(i, len(stones)):
            s2 = stones[j]
            if i == j:
                continue
            if intersect_xy(s1, s2, rmin, rmax):
                cnt += 1

    print('Part1', cnt)

def part2():
    stones = parse()
    # 9 equations and 9 unknowns already from the first 3 points
    x, y, z, dx, dy, dz, t1, t2, t3 = symbols('x y z dx dy dz t1 t2 t3')
    (x0, y0, z0), (dx0, dy0, dz0) = stones[0]
    (x1, y1, z1), (dx1, dy1, dz1) = stones[1]
    (x2, y2, z2), (dx2, dy2, dz2) = stones[2]

    eq1 = Eq(x + t1*dx, x0 + t1*dx0)
    eq2 = Eq(y + t1*dy, y0 + t1*dy0)
    eq3 = Eq(z + t1*dz, z0 + t1*dz0)

    eq4 = Eq(x + t2*dx, x1 + t2*dx1)
    eq5 = Eq(y + t2*dy, y1 + t2*dy1)
    eq6 = Eq(z + t2*dz, z1 + t2*dz1)

    eq7 = Eq(x + t3*dx, x2 + t3*dx2)
    eq8 = Eq(y + t3*dy, y2 + t3*dy2)
    eq9 = Eq(z + t3*dz, z2 + t3*dz2)

    sol = solve([eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9], (x, y, z, dx, dy, dz, t1, t2, t3))
    ret = 0
    for t3 in sol[0][:3]:
        ret += t3
    print("Part2", ret)

part1()
part2()
