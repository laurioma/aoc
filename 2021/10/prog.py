import sys 

closing = {}
closing['('] = ')'
closing['['] = ']'
closing['{'] = '}'
closing['<'] = '>'

closingsc = {}
closingsc[')'] = 3
closingsc[']'] = 57
closingsc['}'] = 1197
closingsc['>'] = 25137

closingsc2 = {}
closingsc2[')'] = 1
closingsc2[']'] = 2
closingsc2['}'] = 3
closingsc2['>'] = 4

def check2(str):
    opening = []
    for i in range(len(str)):
        if str[i] in closing.keys():
            opening.append(str[i])
        elif str[i] in closing.values():
            if str[i] == closing[opening[-1]]:
#                print('okclosing',i, opening[-1], str[i])
                opening.pop()
            else:
#                print('errclosing',i, opening[-1], str[i])
                return (str[i], False)
    return ('', True)

def check3(str):
    opening = []
    for i in range(len(str)):
        if str[i] in closing.keys():
            opening.append(str[i])
        elif str[i] in closing.values():
            if str[i] == closing[opening[-1]]:
#                print('okclosing',i, opening[-1], str[i])
                opening.pop()
            else:
                assert False
        else:
            assert False
    return opening

def run(part2):
    lines = open(sys.argv[1]).read().splitlines()
    answ = 0
    incompl = []
    for l in lines:
        ret = check2(l)
        if not ret[1]:
            answ += closingsc[ret[0]]
        else:
            incompl.append(l)

    print("Part1", answ)

    scores = []
    for l in incompl:
        ret = check3(l)
        score = 0
#        print(ret)
        for r in reversed(ret):
            score *= 5
            score += closingsc2[closing[r]]
#            print(score, closing[r], closingsc2[closing[r]])
        scores.append(score)
    scores.sort()
    middle = scores[int(len(scores)/2)]
    print("Part2", middle)

run(0) if len(sys.argv) < 3 or sys.argv[2] == "1" else run(1)

