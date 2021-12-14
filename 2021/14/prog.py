import sys

def getinput():
    lines = open(sys.argv[1]).read().splitlines()
    templ = ""
    getinstr = False
    rules = []
    for l in lines:
        if l.strip() == "":
            getinstr = True
            continue

        if not getinstr:
            templ = l.strip()

        else:
            i = l.split(' -> ')
            rules.append((i[0], i[1]))
#    print(templ, rules)
    return (templ, rules)

def part1():
    templ, rules = getinput()
    newt = templ
    for s in range(10):
        inserted = 0
        for i in range(1,len(templ)):
            for r in rules:
                if r[0] == templ[i-1:i+1]:
                    idx = i + inserted
                    newt = newt[0:idx] + r[1] + newt[idx:]
                    inserted+=1

#        print ("round", s+1, newt, len(newt))
        templ = newt
    tset = set(templ)
    counts = []
    for t in tset:
        counts.append(templ.count(t))
#    print (tset, counts)
    counts.sort()
    print("Part1", counts[-1] - counts[0])

def part2():
    templ, rules = getinput()

    pairs = {}
    for i in range(1, len(templ)):
        k = templ[i-1:i+1]
        if k in pairs:
            pairs[k] += 1
        else:
            pairs[k] = 1

#    print(pairs)
    border1 = templ[0]
    border2 = templ[-1]

    for s in range(40):
        deleted = {}
        for r in rules:
            if r[0] in pairs:
                deleted[r[0]] = (r[1], pairs[r[0]])
                del pairs[r[0]]
#        print("del", deleted, pairs)

        for d in deleted:
            k1 = d[0] + deleted[d][0]
            k2 = deleted[d][0] + d[1]
            if k1 in pairs:
                pairs[k1] += deleted[d][1]
            else:
                pairs[k1] = deleted[d][1]
            if k2 in pairs:
                pairs[k2] += deleted[d][1]
            else:
                pairs[k2] = deleted[d][1]
#            print("ins", k1, k2, pairs)

    cnt={}
    for p in pairs:
        if p[0] not in cnt:
            cnt[p[0]] = 0
        cnt[p[0]] += pairs[p]
        if p[1] not in cnt:
            cnt[p[1]] = 0
        cnt[p[1]] += pairs[p]

    # every characrter except border ones are now counted twice
    cnt[border1] += 1
    cnt[border2] += 1
    for c in cnt:
        cnt[c] /= 2
#        print(cnt)

    counts = []
    for c in cnt:
        counts.append(cnt[c])
    counts.sort()
#        print (counts)
    print("Part2", counts[-1] - counts[0])
        
part1() if len(sys.argv) < 3 or sys.argv[2] == "1" else part2()