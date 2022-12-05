import sys 
import re

NSTACKS=9

def part(part):
    read_crates = True
    stacks = []
    for sidx in range(NSTACKS):
        stacks.append([])
    with open(sys.argv[1]) as f:
        for line in f:
            l = line
            if read_crates:
                if l[1] == '1':
                    read_crates = False
                else:
                    for sidx in range(NSTACKS):
                        lidx = 4*sidx+1
                        if l[lidx] != ' ':
                            stacks[sidx].append(l[lidx])
            else:
                if l.strip() == '':
                    continue; 
                m = re.search('move (\d+) from (\d+) to (\d+).*', l)
                assert(m)
                ncrates = int(m.group(1))
                sstack = int(m.group(2))-1
                dstack = int(m.group(3))-1
                if part == 1:
                    for n in range(ncrates):
                        cr = stacks[sstack].pop(0)
                        stacks[dstack].insert(0, cr)
                else:
                    for n in range(ncrates):
                        cr = stacks[sstack].pop(ncrates-n-1)
                        stacks[dstack].insert(0, cr)

    answer = ''
    for i in range(NSTACKS):
        answer+=stacks[i][0]
    print ('Part%d %s'% (part, answer))

part(1)
part(2)