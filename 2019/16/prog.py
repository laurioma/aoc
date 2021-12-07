import sys
import time
import re

def get_coeffs(coeffs, step, outl):
    outcoeffs = []
    for i in range(outl):
        outcoeffs.append(coeffs[int((i+1)/(step+1)) % len(coeffs)])
#    print("step", step, outcoeffs)
    return outcoeffs

def execute(file, part2):
    phases = 100 if len(sys.argv) < 4 else int(sys.argv[3])
    with open(file) as f:
        lines = f.readlines()
    invec = []
    for i in range(len(lines[0].rstrip())):
        invec.append(int(lines[0][i]))

    if part2:
        iv = invec.copy()
        print("len b4", len(invec))
        for i in range(1):
            invec += iv
        print("len af", len(invec))
    else:
        print(invec)

    coeffs = [0, 1, 0, -1]
    for i in range(phases):
        print("phase", i)
        for j in range(int(len(invec)/2)):
            mulvec = invec.copy()
            mulcoeffs = get_coeffs(coeffs, j, len(invec))
            for k in range(len(mulcoeffs)):
                mulvec[k] *= mulcoeffs[k]
                print(j, invec[k], "*=", mulcoeffs[k], "-> ", mulvec[k], end = ' ')
            print()
            res = 0
            for l in range(len(invec)):
                res += mulvec[l]
            if j < len(invec):
                invec[j] = abs(res) % 10
#            print ("sum", res, "mod", invec[j])
        print(invec)
    astr = ""
    for i in range(8): 
        astr+=str(invec[i])
    print("Answer", astr)

execute(sys.argv[1], int(sys.argv[2]))
#coeffs = [0, 1, 0, -1]
#for s in range(8):
#    get_coeffs(coeffs, s, 8)
