import sys 
import re

def check_marker(l, idx, max):
    s = set()
    for i in range(idx-max+1, idx+1):
        s.add(l[i])
    return len(s) == max

def part(part):
    res = 0
    with open(sys.argv[1]) as f:
        for line in f:
            l = line
            chlen = 4
            if part == 2:
                chlen = 14
            for i in range(chlen-1, len(l)):
                if check_marker(l, i, chlen):
                    #print("found", l, i+1)
                    res = i+1
                    break
    print ('Part%d %s'% (part, res))

part(1)
part(2)