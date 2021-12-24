import sys
from random import randrange
import cProfile

REGS = {'w', 'x', 'y', 'z'}

def run_prog(prog, input):
    vars = {}
    originp = input
    for r in REGS:
        vars[r] = 0
    for i, instr in enumerate(prog):
        if instr[0] == "inp":
            assert(instr[1] in REGS)
            vars[instr[1]] = int(input[0])
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
    return vars

def analyze_prog(prog):
    vars = {}
    for r in REGS:
        vars[r] = 0

    inputidx = 0
    for i, instr in enumerate(prog):
        op = instr[0]
        arg1 = vars[instr[1]]            
        assert(instr[1] in REGS)
        arg2 = None
        if len(instr) == 3:
            if instr[2] in REGS:
                arg2 = vars[instr[2]]
            else:
                arg2 = int(instr[2])

        if op == "inp":
            vars[instr[1]] = [op, inputidx]
            inputidx+=1
        elif op == "add":
            if arg1 == 0 and arg2 == 0:
                vars[instr[1]] = 0
            elif isinstance(arg1, int) and isinstance(arg2, int):  
                vars[instr[1]] = arg1 + arg2
            elif arg1 == 0 or arg2 == 0:
                if arg1 == 0:
                    vars[instr[1]] = arg2
                else:
                    vars[instr[1]] = arg1
            else:
                vars[instr[1]] = [op, arg1, arg2]
        elif op == "mul":
            if arg1 == 0 or arg2 == 0:
                vars[instr[1]] = 0
            elif arg1 == 1 or arg2 == 1:
                if arg1 == 1:
                    vars[instr[1]] = arg2
                else:
                    vars[instr[1]] = arg1
            elif isinstance(arg1, int) and isinstance(arg2, int):
                vars[instr[1]] = arg1 * arg2
            else:
                vars[instr[1]] = [op, arg1, arg2]
        elif op == "div":
            assert(arg2 != 0)
            if arg1 == 0:
                vars[instr[1]] = 0
            elif isinstance(arg1, int) and isinstance(arg2, int):
                vars[instr[1]] = arg1 / arg2
            elif arg2 == 1:
                vars[instr[1]] = arg1
            else:
                vars[instr[1]] = [op, arg1, arg2]
        elif op == "mod":
            if arg1 == 0:
                vars[instr[1]] = 0
            elif isinstance(arg1, int) and isinstance(arg2, int):
                vars[instr[1]] = arg1 % arg2
            else:                
                vars[instr[1]] = [op, arg1, arg2]
        else:
            assert(op == "eql")
            if arg1 == 0 and arg2 == 0:
                vars[instr[1]] = 1
            elif isinstance(arg1, int) and isinstance(arg2, int):
                vars[instr[1]] = arg1 == arg2
            elif isinstance(arg1, int) or isinstance(arg2, int):
                intval = arg1 if isinstance(arg1, int) else arg2
                expr = arg2 if isinstance(arg1, int) else arg1
                if expr[0] == "eql" and  intval not in [0, 1]:
                    vars[instr[1]] = 0
                else:
                    vars[instr[1]] = [op, arg1, arg2]
            else:                
                vars[instr[1]] = [op, arg1, arg2]
    return vars


def run(part2):
    lines = open(sys.argv[1]).read().splitlines()
    print(lines)
    prog = []
    for l in lines:
        prog.append(l.split())

    state = analyze_prog(prog)
    print(state)

run(0) if len(sys.argv) < 3 or sys.argv[2] == "1" else run(1)
