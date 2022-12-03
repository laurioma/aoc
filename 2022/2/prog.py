import sys 

OPPONENT_MAP = {'A':'R', 'B':'P', 'C':'S'}
MY_MAP = {'X':'R', 'Y':'P', 'Z':'S'}
RESULT_MAP = {'R': ['S', 'P', 'R'], 'P': ['R', 'S', 'P'], 'S': ['P', 'R', 'S']}
SCORES_SIGN={'R':1,'P':2,'S':3}

def part1():
    with open(sys.argv[1]) as f:
        score = 0
        for line in f:
            l = line.strip()
            op = l[0]
            my = l[2]
            op_sign = OPPONENT_MAP[op]
            my_sign = MY_MAP[my]
            # lose
            if my_sign == RESULT_MAP[op_sign][0]:
                score += 0 + SCORES_SIGN[my_sign]
            # win
            elif my_sign == RESULT_MAP[op_sign][1]:
                score += 6 + SCORES_SIGN[my_sign]
            # draw
            else: 
                score += 3 + SCORES_SIGN[my_sign]
    print ('Part1', score)


def part2():
    with open(sys.argv[1]) as f:
        score = 0
        for line in f:
            l = line.strip()
            op = l[0]
            my = l[2]
            op_sign = OPPONENT_MAP[op]
            #lose
            if my == 'X':
                my_sign_new = RESULT_MAP[op_sign][0]
                score += 0 + SCORES_SIGN[my_sign_new]
            #draw
            elif my == 'Y':
                my_sign_new = RESULT_MAP[op_sign][2]
                score += 3 + SCORES_SIGN[my_sign_new]
            #win
            else:
                my_sign_new = RESULT_MAP[op_sign][1]
                score += 6 + SCORES_SIGN[my_sign_new]
    print ('Part2', score)

part1()
part2()