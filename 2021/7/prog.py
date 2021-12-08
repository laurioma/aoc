import sys 

def run(part2):
    with open(sys.argv[1]) as f:
        for line in f:
            submarines = [int(l) for l in line.split(',')]
        submarines.sort()
        print(submarines)
        minsum = sys.maxsize
        bestpos = 0
        minpos = submarines[0]
        maxpos = submarines[-1]
        for pos in range(minpos, maxpos + 1):
            sum = 0
            for i in range(len(submarines)):
                if part2:
                    move = abs(submarines[i] - pos)
                    step = 0
                    for s in range(1, move + 1):
                        step += s
                    sum += step
                    #print (pos, i, "sum", sum, "step", step, "best", bestpos, minsum)
                else:
                    sum += abs(submarines[i] - pos)
                    #print (pos, i, sum, bestpos, minsum)
            if minsum > sum:
                bestpos = pos
                minsum = sum
        print(bestpos, minsum)

run(0) if len(sys.argv) < 3 or sys.argv[2] == "1" else run(1)