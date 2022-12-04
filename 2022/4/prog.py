import sys 
import re

def in_range(r1, r2):
    if r1[0] <= r2[0] and r1[1] >= r2[1]:
        return True
    return False

def overlap(r1, r2):
    if r1[0] <= r2[0] and r1[1] >= r2[0] or r1[0] <= r2[1] and r1[1] >= r2[1]:
        return True
    return False

def part(part):
    score = 0
    with open(sys.argv[1]) as f:
        for line in f:
            l = line.strip()
            m = re.search('(\d+)-(\d+),(\d+)-(\d+)', l)
            assert(m)
            r1 = (int(m.group(1)), int(m.group(2)))
            r2 = (int(m.group(3)), int(m.group(4)))
            if part==2:
                if overlap(r1, r2) or overlap(r2,r1):
                    score +=1
            else:
                if in_range(r1, r2) or in_range(r2,r1):
                    score +=1

    print ('Part%d %d'%(part,score))

part(1)
part(2)