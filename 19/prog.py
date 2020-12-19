import sys
import time
import re
import copy

def bfs(rulel, string):
    vlog = 0

    if vlog:
        print("BFS", rulel, string)
    if len(rulel) > len(string):
        if vlog:
            print("*BFS3 FAIL",len(rulel), len(string))
        return False
    elif len(rulel) == 0 or len(string) == 0:
        ret = len(rulel) == 0 and len(string) == 0
        if vlog:
            print("*BFS2 ", "OK" if ret else "FAIL")
        return ret

    s = rulel.pop(0) 
    if vlog:
        print ('POP', s, rulel) 

    if isinstance(s, str):
        if string[0] == s:
            if vlog:
                print("MATCH", s, rulel)
            return bfs(rulel, string[1:])
    else:
        for neighbour in rules[s]:
            if vlog:
                print("nn", neighbour, "->", list(neighbour) + rulel)
            if bfs(list(neighbour) + rulel, string):
                if vlog:
                    print ("*BFS1 OK")
                return True
    if vlog:
        print("BFS0 FAIL")
    return False

rules = {}


def execute(file, part2):
    data = ""
    with open(file) as f:
        data = f.read()
    rows = data.split('\n')

    text = []
    rulet = []
    addtext = False
    for r in rows:
        if r == "":
            addtext = True
            continue
        if not addtext:
            rulet.append(r)
            m = re.search("(\d+): \"(.*)\"", r.rstrip())
            if m:
                rules[int(m.group(1))] = m.group(2)
            else:
                m = re.search("(\d+): (.*)$", r.rstrip())
                if m:
                    orrules = m.group(2).split("|")
                    rules[int(m.group(1))] = []
                    for andstr in orrules:
                        andr_s = andstr.split(" ")
                        andl = []
                        for andr in andr_s:
                            if andr != "":
                                andl.append(int(andr))
                        rules[int(m.group(1))].append(andl)
                else:
                    assert(False), r
        else:
            text.append(r)

#    for k in sorted(rulet, key=lambda x: int(x[:x.index(':')])):        
#        print(k)

    for r in sorted(rules):
        print(r, rules[r])

    count = 0
    for line in text:
        print ("START", line, end = ' ')
        m = bfs(list(rules[0][0]), line)
        if m:
            print("\t\t\t\t\tOK")
            count+=1
        else:
            print("\t\t\t\t\tFAIL")


    print("RESULT", count)

f = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
p2 = 0 if len(sys.argv) < 3 else int(sys.argv[2])
execute(f, p2)