import sys 

def part1():
    lines = open(sys.argv[1]).read().splitlines()
    nbits = len(lines[0])
    cnt1 = [0] * nbits
    for line in lines:
        for idx in range(nbits):
            if line[idx] == '1':
                cnt1[idx] += 1
    gstr = ''.join(['1' if c > (len(lines) / 2) else '0' for c in cnt1])
    estr = ''.join(['1' if c < (len(lines) / 2) else '0' for c in cnt1])
    ansg = int(gstr, 2)
    anse = int(estr, 2)
    print(anse, ansg, ansg * anse)

def part2_1(lines, oxn):
    nbits = len(lines[0])
    for i in range(nbits):
        #print("i", i)
        cnt1 = [0] * nbits
        for line in lines:
            for idx in range(nbits):
                if line[idx] == '1':
                    cnt1[idx] += 1
        lines2 = []
        for lid in range(len(lines)):
            # keep 1s
            if (oxn and cnt1[i] >= len(lines) / 2) or (oxn == 0 and cnt1[i] < len(lines) / 2) :
                if lines[lid][i] == '1':
                    lines2.append(lines[lid])
            else:
                if lines[lid][i] == '0':
                    lines2.append(lines[lid])
        #print('lines2', lines2)
        lines = lines2
        if len(lines) <= 1:
            break

    oxn = int(lines[0], 2)
    return oxn

def part2():
    lines = open(sys.argv[1]).read().splitlines()
    oxn = part2_1(lines, 1)
    co2 = part2_1(lines, 0)
    print("oxn", oxn, co2, oxn*co2)
  
part1() if len(sys.argv) < 3 or sys.argv[2] == "1" else part2()