import sys
from random import randrange
from collections import defaultdict

REGS = {'w', 'x', 'y', 'z'}

def run_prog(prog, input, vars = None):
    if vars == None:
        vars = {}
        for r in REGS:
            vars[r] = 0
    originp = input
    inpidx = 0
    for i, instr in enumerate(prog):
        if instr[0] == "inp":
            assert(instr[1] in REGS)
            vars[instr[1]] = int(input[0])
            # print("inp", inpidx, vars['z'])
            inpidx+=1
            input = input[1:]
        elif instr[0] == "add":
            assert(instr[1] in REGS)
            if instr[2] in REGS:
                vars[instr[1]] += vars[instr[2]]
            else:
                vars[instr[1]] += int(instr[2])
        elif instr[0] == "mul":
            assert(instr[1] in REGS)
            if instr[2] in REGS:
                vars[instr[1]] *= vars[instr[2]]
            else:
                vars[instr[1]] *= int(instr[2])
        elif instr[0] == "div":
            assert(instr[1] in REGS)
            if instr[2] in REGS:
                vars[instr[1]] = int(vars[instr[1]]/vars[instr[2]])
            else:
                vars[instr[1]] = int(vars[instr[1]]/int(instr[2]))
        elif instr[0] == "mod":
            assert(instr[1] in REGS)
            if instr[2] in REGS:
                vars[instr[1]] = int(vars[instr[1]] % vars[instr[2]])
            else:
                vars[instr[1]] = int(vars[instr[1]] % int(instr[2]))
        else:
            assert(instr[0] == "eql")
            assert(instr[1] in REGS)
            if instr[2] in REGS:
                vars[instr[1]] = int(vars[instr[1]] == vars[instr[2]])
            else:
                vars[instr[1]] = int(vars[instr[1]] == int(instr[2]))
    # rl = list(REGS)
    # rl.sort()
    # print(originp)
    # for r in rl:
    #     print(r, vars[r], end='|')
    # print()
    return vars['z']

def process_digit2(w, zi, div, add, add2):
    # print("test",level,w,zi, div, add, add2)
    z = zi
    x=z%26
    z=int(z/div)
    x+=add
    x= x != w
    y=x*25
    y+=1
    z=z*y
    y=w + add2
    y*=x
    z+=y
    return z

# the single digit validation function translated to python
def process_digit(w, z, div, add, add2):
    if z % 26 + add == w:
        return int(z/div)
    else:
        return w + add2 + int(z/div) * 26 

# returns what z had to be to get zout from process_digit
def get_process_digit_inputz(w, zout, div, add, add2):
    # if (z % 26) + add == w:
    #     return int(z/div)
    # zout = z/div => zin = zout * div 
    for j in range(div):
        zin = zout * div + j
        if process_digit(w, zin, div, add, add2) == zout:
            return True, zin

    # if z % 26 + add != w:
    #     return w + add2 + int(z/div) * 26 
    for j in range(div):
        zin = int((zout - w - add2)/26*div + j)
        if process_digit(w, zin, div, add, add2) == zout:
            return True, zin

    return False, 0


def check_num(progs, part2, idx, reqz, numstr):
    rng = range(1,10) if part2 else range(9,0, -1)
    for i in rng:
        prg = progs[idx]
        div = int(prg[4][2])
        add = int(prg[5][2])
        add2 = int(prg[15][2])

        ok, reqz2 = get_process_digit_inputz(i, reqz, div, add, add2)
        if not ok:
            continue

        if idx > 0:
            ok, numstr2 = check_num(progs, part2, idx-1, reqz2, str(i) + numstr)
            if ok:
                return ok, numstr2
        else:
            # at the start we must have 0 in z reg
            assert(reqz2 == 0)
            return True, str(i) + numstr 

    return False, ""

def run(part2):
    lines = open(sys.argv[1]).read().splitlines()
#    print(lines)
    prog = []
    progs = []
    for l in lines:
        prog.append(l.split())
        if l.find("inp") >= 0:
            progs.append([])
        progs[-1].append(l.split())
        

    ok, num = check_num(progs, part2, 13, 0, "")
    if ok:
        print ("Part", "2" if part2 else "1", num, "check", run_prog(prog, num))
    else:
        print("Part", "2" if part2 else "1","Failed")

run(0)
run(1)
