import sys 

def check_hmirror(lines, yy):
    errcnt = 0
    for dy in range(yy+1):
        yu = yy - dy
        yd =  yy + dy + 1
        if 0 <= yu < len(lines) and 0 <= yd < len(lines):
            for x in range(len(lines[0])):
                if lines[yu][x] != lines[yd][x]:
                    errcnt += 1
    return errcnt

def run(npart):
    patterns = open(sys.argv[1]).read().split('\n\n')
    score = 0
    for i, p in enumerate(patterns):
        lines = p.splitlines()
        lines = [list(l) for l in lines]
        for scorecoef in [100, 1]:
            for y in range(len(lines)-1):
                errcnt = check_hmirror(lines, y)
                if errcnt == npart - 1:
                    score += scorecoef * (y+1) 

            if scorecoef == 100:
                # transpose
                lines = [list(i) for i in zip(*lines)]

    print('Part'+str(npart), score)

run(1)
run(2)