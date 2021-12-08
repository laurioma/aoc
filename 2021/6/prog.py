import sys

days = 256
def part1():
    with open(sys.argv[1]) as f:
        for line in f:
            fishesstr = line.split(',')
            print(fishesstr)
        fishes = []
        for f in fishesstr:
            fishes.append(int(f))
        for d in range(days):
            newfish = []
            for f in fishes:
                nf = f - 1 if f > 0 else 6
                newfish.append(nf)
            lennf = len(newfish)
            for nfi in range(lennf):
                if newfish[nfi] == 6 and fishes[nfi] == 0:
                    newfish.append(8)
            if d < 18:
                print(d, newfish)
            fishes = newfish
        print(len(fishes))

def part2():
    with open(sys.argv[1]) as f:
        for line in f:
            fishesstr = line.split(',')
            print(fishesstr)
        fishes = {}
        for f in fishesstr:
            fi = (int(f), 0)
            fishes[fi] = fishes[fi] + 1 if fi in fishes else 1
        print(fishes)

        for d in range(days):
            newfish = {}
            for f in fishes:
                if f[0] > 0:                    
                    nf = f[0] - 1
                    newfish[nf, f[1]] = fishes[f]
                else:
                    nf = 6
                    if (nf, 0) in newfish:
                        newfish[nf, 0] += fishes[f]
                    else:
                        newfish[nf, 0] = fishes[f]
#                print ('dbg', f, nf, fishes[f], newfish)
            #print(fishes, newfish)
            fkeys = [f for f in newfish]
            for nfi in fkeys:
                if nfi == (6, 0):
                    newfish[8, 1] = newfish[nfi]
            if d < 18:
                print(d, newfish)
            fishes = newfish
        fcount = 0
        for f in fishes:
            fcount += fishes[f]
        print(fcount)

part1() if len(sys.argv) < 3 or sys.argv[2] == "1" else part2()