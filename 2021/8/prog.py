import sys 

def resolve(list):
    setmap = {}
    for l in list:
        if len(l) == 2:
            setmap[1] = l
        elif len(l) == 3:
            setmap[7] = l
        elif len(l) == 4:
            setmap[4] = l
        elif len(l) == 7:
            setmap[8] = l
    for l in list:
        if len(l) == 6 and not setmap[1].issubset(l):
            setmap[6] = l
        elif len(l) == 5 and setmap[1].issubset(l):
            setmap[3] = l
    seg2 = setmap[3] - setmap[6]
    for l in list:
        if len(l) == 5 and seg2.issubset(l) and l != setmap[3]:
            setmap[2] = l
        elif len(l) == 5 and not seg2.issubset(l):
            setmap[5] = l
    for l in list:
        if len(l) == 6 and setmap[5].issubset(l) and l != setmap[6]:
            setmap[9] = l
        elif len(l) == 6 and not setmap[5].issubset(l):
            setmap[0] = l
    return setmap

def run(part2):
    i = open(sys.argv[1]).read()
    i = i.replace("|\n", "|")
    lines = i.splitlines()
    answ = 0
    for i in range(len(lines)):
        sline = lines[i].split('|')
        nums = sline[1].split()
        if not part2:
            for n in nums:
                if len(n) in [2, 4, 3, 7]:
                    answ += 1
        else:
            example_sets = [set(s) for s in sline[0].split()]
            resolved_examples = resolve(example_sets)
            res_sets = [set(s) for s in sline[1].split()]
#            print ("res", res_sets)
            ress = ''
            for r in res_sets:
                for i in range(10):
                    #print(i, "check", r, resolved_examples[i], r == resolved_examples[i])
                    if r == resolved_examples[i]:
                        ress += str(i)
 #           print(res_sets, ress, int(ress), answ)
            answ += int(ress)
    print(answ)

run(0) if len(sys.argv) < 3 or sys.argv[2] == "1" else run(1)

