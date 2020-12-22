import sys
import time
import copy
import re
import itertools

# find all lines containi
def execute(file, partnr):
    global nump
    data = ""
    with open(file) as f:
        data = f.read()

    rows = data.split('\n')

    allingrs = set()
    allallergs = {}
    foods = []
    for fid in range(len(rows)):
        row = rows[fid]
        s = row.split('(')
        ingr = s[0].rstrip().split(" ")

        for i in ingr:
            allingrs.add(i)

        m = re.search("contains (.*)\)", s[1])
        assert(m)
        allerg = m.group(1).split(", ")

        for a in allerg:
            if a not in allallergs:
                allallergs[a] = set(ingr)
            else:
                allallergs[a] &= set(ingr)
        foods.append((ingr,allerg))

    print (allallergs)

    okingrs = set()
    for ingr in allingrs:
        gen = (ingr in x for x in allallergs.values())
        isany = any(gen)
#        print ("ingr", ingr , "is allerg", isany)
        ok = not isany
        if ok:
            okingrs.add(ingr)

    count = 0
    for i, a in foods:
        for ingr in i:
            if ingr in okingrs:
                count += 1
    print("Answer1", count)

    assignments = {}
    while len(assignments) < len(allallergs):
        for a in allallergs:
            r = [x for x in allallergs[a] if x not in assignments]
#            print ("r", r)
            if len(r) == 1:
#                print ("r==1", r[0])
                assignments[r[0]] = a
                break
    print(assignments)

    print("Answer2", end=' ')
    v = sorted(assignments, key=lambda x: assignments[x])
    print(",".join(v))

f = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
p2 = 0 if len(sys.argv) < 3 else int(sys.argv[2])

execute(f, p2)