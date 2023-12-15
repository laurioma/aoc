import sys 
from collections import defaultdict

def hash(str):
    cv = 0
    for c in str:
        cv += ord(c)
        cv *= 17
        cv %= 256
    return cv

def part1():
    lines = open(sys.argv[1]).read().splitlines()
    score = 0
    for line in lines:
        split = line.split(',')
        for s in split:
            score += hash(s)
    print('Part1', score)


def part2():
    lines = open(sys.argv[1]).read().splitlines()
    for line in lines:
        split = line.split(',')
        boxes = defaultdict(list)
        for s in split:
            iseq = s.count('=') > 0
            val = s.split('=')[1] if iseq else ''
            label = s.split('=')[0] if iseq else s.split('-')[0]
            boxi = hash(label)
            if iseq:
                result = list(filter(lambda x: x[0] == label, boxes[boxi]))
                assert len(result) <= 1
                if len(result) == 1:
                    for l in boxes[boxi]:
                        if l[0] == label:
                            l[1] = val
                            break
                else:
                    boxes[boxi].append([label, val])
            else:
                boxes[boxi] = list(filter(lambda x: x[0] != label, boxes[boxi]))
    score = 0
    for k in boxes:
        for i, l in enumerate(boxes[k]):
            score += ((k+1)*(i+1) * int(l[1]))
    print('Part2', score)

part1()
part2()
