import sys
import time
import re
import copy

def check_value(value, fields):
    fail = 0
    for key in fields:
        f = fields[key]
#        print ("check ", value, f[0], f[1], f[2], f[3])
        if (value < f[0] or value > f[1]) and (value < f[2] or value > f[3]):
            fail += 1
        if fail == len(fields):
 #           print ("ALL FAIL")
            return False
 #       print("PASS")
    return True

def prune_fitting(fittings, nr):
    pruned = False
    for f in fittings:
        if nr in fittings[f] and len(fittings[f]) > 1:
            fittings[f].remove(nr)
            print("pruning", nr, "from", f)
            pruned = True
    return pruned

def execute(file, part2):
    fields = {}
    myt = []
    others = []
    state = 0
    valid = []
    with open(file) as f:
        for line in f:
            if line.rstrip() != "":
                if state == 0:
                    m = re.search("([^:]+): (\d+)-(\d+) or (\d+)-(\d+)", line)
                    if m:
                        fields[m.group(1)] = [int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))]
                    else:
                        print("error", line)
                elif state == 1:
                    state += 1
                elif state == 2:
                    for n in line.rstrip().split(","):
                        myt.append(int(n))
                elif state == 3:
                    state += 1
                elif state == 4:
                    t = []
                    for n in line.rstrip().split(","):
                        t.append(int(n))
                    others.append(t)
            else:
                state += 1

    print(fields, "my", myt, "others", others)

    checksum = 0
    for values in others:
        fail = 0
        for value in values:
            if not check_value(value, fields):
                print ("val error", value, checksum)
                checksum += value
                fail = 1
        if not fail:
            valid.append(values)
    print("answer p1", checksum)

    print ("valid", valid)

    fitting = {}
    for key in fields:
        f = fields[key]
        fitting[key] = []
        for i in range(len(valid[0])):
            ok = True
            for v in valid:
                if (v[i] < f[0] or v[i] > f[1]) and (v[i] < f[2] or v[i] > f[3]):
#                    print ("fail", i, v, key, fields)
                    ok = False
                    break
            if ok:
                fitting[key].append(i)
            print("field ", key, " for ", i, ":", ok)
    print ("f", fitting)
    pruned = True
    while pruned:
        pruned = False 
        for f in fitting:
            if len(fitting[f]) == 1:
                if (prune_fitting(fitting, fitting[f][0])):
                    pruned = True
    print ("f", fitting)
    answer2 = 0
    for f in fitting:
        if f[0:9] == "departure":
            if answer2 == 0:
                answer2 = myt[fitting[f][0]]
            else:
                answer2 *= myt[fitting[f][0]]
            print("my", f, fitting[f][0], myt[fitting[f][0]])

    print("Answer2", answer2)

execute(sys.argv[1], int(sys.argv[2]))