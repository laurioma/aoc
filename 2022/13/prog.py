import sys
from functools import cmp_to_key

RIGHT = -1
EQ = 0
WRONG = 1

def comp(l1, l2):
    if isinstance(l1, list) and isinstance(l2, list):
        for i in range(len(l1)):
            # right run out first
            if len(l2) <= i:
                return WRONG
            if isinstance(l1[i], int) and isinstance(l2[i], int):
                # left is bigger
                if l1[i] > l2[i]:
                    return WRONG
                elif l1[i] < l2[i]:
                    return RIGHT
            elif isinstance(l1[i], list) and isinstance(l2[i], list):
                r = comp(l1[i], l2[i])
                if r != EQ:
                    return r
            elif isinstance(l1[i], list) and isinstance(l2[i], int):
                r = comp(l1[i], [l2[i]])
                if r != EQ:
                    return r
            elif isinstance(l1[i], int) and isinstance(l2[i], list):
                r = comp([l1[i]], l2[i])
                if r != EQ:
                    return r
            else:
                assert(False)
        # left run out first
        if len(l1) < len(l2):
            return RIGHT
        assert(len(l1) == len(l2))
        return EQ

def run():
    lineg = open(sys.argv[1]).read().replace('\r','').split('\n\n')
    rightidx = []
    for (i,l) in enumerate(lineg):
        ll = l.splitlines()
        l1 = eval(ll[0]) 
        l2 = eval(ll[1])
        r = comp(l1, l2)
        if r == RIGHT:
            rightidx.append(i+1)

    print ('Part1', sum(rightidx))

    lines = open(sys.argv[1]).read().replace('\r','').replace('\n\n','\n').splitlines()
    exprs = []
    for l in lines:
        exprs.append(eval(l))
    exprs.append([[2]])
    exprs.append([[6]])

    exprs.sort(key=cmp_to_key(comp))

    idx1 = -1
    idx2 = -1
    for (i,e) in enumerate(exprs):
        if e == [[2]]:
            idx1 = i+1
        if e == [[6]]:
            idx2 = i+1
    print ('Part2', idx1*idx2)


run()
