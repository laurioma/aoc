import sys
import time
import copy
import re
import itertools

def maxelem(cands, exclude):
    maxc = 0
    el = None
    for c in cands:
        if c not in exclude:
            if maxc < cands[c]:
                maxc = cands[c]
                el = c
    return el


def findmaxany(cands):
    maxc = 0
    for c in cands:
        if maxc < cands[c]:
            maxc = cands[c]
    return maxc

# list of map of ingr=allerg
def resolve_ingr(allerg_cands):
    res = []
    ingr = {}
    ac = allerg_cands.copy()
#    while len(ingr) < len(allerg_cands):
    while True:
        mapping = {}
#        print ("Start", ac)
        first = True
        for a in sorted(ac,  key=lambda x: findmaxany(ac[x]), reverse=True):
            maxi = maxelem(ac[a], mapping.keys())
            if maxi == None:
                break
#            print(a, findmaxany(ac[a]), a,"=", maxi)
            if maxi not in mapping:
                if first:
                    if ac[a][maxi] == 1:
                        del(ac[a][maxi])
                    else:
                        ac[a][maxi] = ac[a][maxi] - 1
                    first = False
#                print ("ADD ", maxi, a)
                mapping[maxi] = a
        if len(mapping) == len(allerg_cands):
#            print("got mapping", mapping)
            res.append(mapping)
        else:
#            print ("no more", len(mapping), ac)
            break
    print("Resolved", res)
    return res

def try_resolutions(ingr_sets, resl):
    match = None
    for res in resl:
        result = True
        for iset in ingr_sets:
            print ("try", res, "for ", iset)
            check = {}
            for r in res:
                for i in iset[0]:
                    if i in r:
                        check[res[r]] = check.get(res[r], 0) + 1

            print("checking", check, iset[1])
            for ch in iset[1]:
                if ch not in check:
                    print ("FAILED", ch, "not found", res, iset[0])
                    result = False
                    break
 #               elif check[ch] > 1:
 #                   print ("FAILED2", ch, "too many", res, iset[0])
 #                   result = False
 #                   break
            if not result:
                break
        if result:
            match = res
            break
    print("Found match", match)
    return match

def count_noallerg(ingr_sets, noallerg):
    pass

def execute(file, partnr):
    global nump
    data = ""
    with open(file) as f:
        data = f.read()

    allerg_cands={}
    ingrs = set()
    ingr_sets=[]
    rows = data.split('\n')
    for row in rows:
        s = row.split('(')
        ingr = s[0].rstrip().split(" ")
        for i in ingr:
            ingrs.add(i)
        m = re.search("contains (.*)\)", s[1])
        assert(m)
        allerg = m.group(1).split(", ")
        ingr_sets.append([ingr, allerg])
        for a, i in itertools.product(allerg, ingr):
#            print ("iter", a, i)
            if not a in allerg_cands:
                allerg_cands[a] = {}
            allerg_cands[a][i] = allerg_cands[a].get(i, 0) + 1
        print ("acands", allerg_cands)
        print ("ingr_sets", ingr_sets)
    r = resolve_ingr(allerg_cands)
    m = try_resolutions(ingr_sets, r)
    if not m:
        print("NOTHING")
        return

    noallerg = set()
    for i in ingrs:
        if i not in m:
            noallerg.add(i)
    print("NOT", noallerg)

    count = 0
    for iset in ingr_sets:
        for na in noallerg:
            if na in iset[0]:
                count+=1

    print("Answer1", count)

    print("Answer2", end=' ')
    for a in sorted(m,  key=lambda x: m[x]):
        print("{0},".format(a), end='')


f = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
p2 = 0 if len(sys.argv) < 3 else int(sys.argv[2])

execute(f, p2)