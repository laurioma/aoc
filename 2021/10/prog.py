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

def parse(str):
    opening = []
    for i in range(len(str)):
        if str[i] in closing:
            opening.append(str[i])
        elif str[i] in closing.values():
            if str[i] == closing[opening[-1]]:
#                print('okclosing',i, opening[-1], str[i])
                opening.pop()
            else:
#                print('errclosing',i, opening[-1], str[i])
                return (str[i], False, opening)
        else:
            assert False
    return ('', True, opening)

def run(part2):
    lines = open(sys.argv[1]).read().splitlines()
    answ = 0
    incompl = []
    for l in lines:
        sym, ok, _ = parse(l)
        if not ok:
            answ += closingsc[sym]
        else:
            incompl.append(l)

    print("Part1", answ)
#    print(incompl)
    scores = []
    for l in incompl:
        sym, ok, remaining = parse(l)
        score = 0
#        print(ret)
        for r in reversed(remaining):
            score *= 5
            score += closingsc2[closing[r]]
#            print(score, closing[r], closingsc2[closing[r]])
        scores.append(score)
    scores.sort()
    middle = scores[int(len(scores)/2)]
    print("Part2", middle)

run(0) if len(sys.argv) < 3 or sys.argv[2] == "1" else run(1)

