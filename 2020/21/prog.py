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

    all_ingrs = set()
    foods = []
    allergs = {}
    ingrs = {}
    for fid in range(len(rows)):
        row = rows[fid]
        s = row.split('(')
        ingr = s[0].rstrip().split(" ")
        foods.append(set(ingr))

        for i in ingr:
            if i not in ingrs:
                ingrs[i] = set()
            ingrs[i].add(fid)

        for i in ingr:
            all_ingrs.add(i)
        m = re.search("contains (.*)\)", s[1])
        assert(m)
        allerg = m.group(1).split(", ")

        for a in allerg:
            if a not in allergs:
                allergs[a] = set()
            allergs[a].add(fid)

    print("foods", foods)
    print("ingrs", ingrs)
    print("allergs", allergs)

    # map allergens to candidate ingredients
    # ingredient is candidate for allergen if it's present in all the lines where same allergen occurs
    cand = {}
    for a, i in itertools.product(allergs, ingrs):
        if bool(allergs[a].union(ingrs[i])):
#            print ("check if ", i, "allways there for", a)
            # check if i is in all lines with a
            fits = True
            for afood in allergs[a]:
#                print("check", foods[afood])
                if not i in foods[afood]:
#                    print("not")
                    fits=False
                    break
            if fits:
                if a not in cand:
                    cand[a] = set()
                cand[a].add(i)
                print("OK", i, a)

    print("candidates", cand)

    results={}
    while cand:
        resolved = None
        for ac in cand:
            if len(cand[ac]) == 1:
                print("Resolved {0}={1}".format(ac, cand[ac]))
                resolved = cand[ac].pop()
                results[resolved] = ac
                del cand[ac]
                break
        if resolved:
            for ac in cand:
                if resolved in cand[ac]:
                    print("remove from", resolved, cand[ac])
                    cand[ac].remove(resolved)
        else:
            assert(), "resolved nothing" 
    assert(len(cand) == 0)
    print ("Results", results)

    noallerg = set()
    for i in all_ingrs:
        if i not in results:
            noallerg.add(i)
    print("NOT", noallerg)

    count = 0
    for food in foods:
        for na in noallerg:
            if na in food:
                count+=1

    print("Answer1", count)

    print("Answer2", end=' ')
    for a in sorted(results,  key=lambda x: results[x]):
        print("{0},".format(a), end='')
 

f = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
p2 = 0 if len(sys.argv) < 3 else int(sys.argv[2])

execute(f, p2)