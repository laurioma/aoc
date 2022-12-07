import sys 
import re

def calcsum(tree, smallsum):
    sum = 0
    for k in tree.keys():
        if isinstance(tree[k], str):
            sum += int(tree[k])
        else:
            sum += calcsum(tree[k], smallsum)
    if sum <= 100000:
        smallsum[0] += sum
    return sum

def findclosest(tree, needspc, closest):
    sum = 0
    for k in tree.keys():
        if isinstance(tree[k], str):
            sum += int(tree[k])
        else:
            sum += findclosest(tree[k], needspc, closest)
    if sum >= needspc:
        currdiff = sum - needspc
        if closest[0] == 0:
            closest[0] = sum
        else:
            bestddiff = closest[0] - needspc
            if currdiff < bestddiff:
                closest[0] = sum
    return sum

def run():
    tree = {}
    level = tree
    levels = [level]
    with open(sys.argv[1]) as f:
        for line in f:
            l = line.strip()
            m = re.search('\$ cd (.*)', l)
            if m:
                dir = m.group(1)
                if dir == '..':
                    level = levels.pop()
                else:
                    levels.append(level)
                    newd = {}
                    if dir in level:
                        newd = level[dir]
                    level = newd
            elif l == "$ ls":
                pass
            else:
                m = re.search('(\d+) (.*)', l);
                if m:
                    level[m.group(2)] = m.group(1)
                else: 
                    m = re.search('dir (.*)', l);
                    assert m,line
                    level[m.group(1)] = {}

    #print(tree)

    smallsum = [0]
    r = calcsum(tree, smallsum)
    print ('Part1 %s'% smallsum[0])

    fssize = 70000000
    needfree = 30000000
    neededspace = needfree - (fssize - r)

    best = [0]
    r = findclosest(tree, neededspace, best)
    print("Part2", best[0])

run()