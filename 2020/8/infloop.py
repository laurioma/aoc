import sys
import re
import copy

program = []
with open(sys.argv[1]) as f:
    for line in f:
        instr_parts = line.split()
        program.append([instr_parts[0], int(instr_parts[1]), 0])
        print("Appended", len(program), program[len(program)-1][0], program[len(program)-1][1])

def run_program(prog):
    pc = 0
    acc = 0
    while pc < len(prog) and prog[pc][2] == 0:
        print ("exec", pc, prog[pc], "acc", acc)
        prog[pc][2] = 1
        if (prog[pc][0] == "nop"):
            pc += 1
        elif (prog[pc][0] == "acc"):
            acc += prog[pc][1]
            pc += 1
        elif (prog[pc][0] == "jmp"):
            pc += prog[pc][1]

    print ("prog return, pc", pc, "acc", acc)
    if (pc == len(prog)):
        return True
    else:
        return False

print("Part1")

run_program(copy.deepcopy(program))

print("Part2")

for i in range(len(program)):
    fixed_prog = copy.deepcopy(program)
    if fixed_prog[i][0] == "jmp":
        print("try fix", i)
        fixed_prog[i][0] = "nop"
        if (run_program(fixed_prog)):
            print("FIXED")
            break
    