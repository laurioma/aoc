import sys 

def check_hmirror(lines, yy):
    hmirror = True
    didcheck = False
    errors = set()
    for dy in range(yy+1):
        yu = yy - dy
        yd =  yy + dy + 1
        if yu >= 0 and yu < len(lines) and yd >= 0 and yd < len(lines):
            didcheck = True
            match = True
            for x in range(len(lines[0])):
                if lines[yu][x] != lines[yd][x]:
                    errors.add((x, yu))
                    match = False
            if not match:
                hmirror = False

    return hmirror and didcheck, errors

def run(npart):
    patterns = open(sys.argv[1]).read().split('\n\n')
    score = 0
    for i, p in enumerate(patterns):
        lines = p.splitlines()
        lines = [list(l) for l in lines]
        for y in range(len(lines)):
            chk, err = check_hmirror(lines, y)
            if (chk and npart == 1) or (not chk and len(err) == 1 and npart == 2):
                score += 100 * (y+1) 
        # transpose
        lines = [list(i) for i in zip(*lines)]

        for y in range(len(lines)):
            chk, err = check_hmirror(lines, y)
            if (chk and npart == 1) or (not chk and len(err) == 1 and npart == 2):
                score += (y+1)       

    print('Part'+str(npart), score)

run(1)
run(2)