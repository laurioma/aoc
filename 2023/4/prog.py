import sys 

def part1():
    lines = open(sys.argv[1]).read().splitlines()
    fscore = 0
    for l in lines:
        a = l.split(':')
        aa = a[1].split('|')
        n1 = set(int(i) for i in aa[0].strip().split())
        n2 = set(int(i) for i in aa[1].strip().split())
        score = 0
        for c in n2:
            if c in n1:
                if score == 0:
                    score = 1
                else:
                    score *=2
        fscore += score
    print('Part1', fscore)

def part2():
    lines = open(sys.argv[1]).read().splitlines()
    cards = {}
    for i,l in enumerate(lines):
        a = l.split(':')
        aa = a[1].split('|')
        n1 = set(int(i) for i in aa[0].strip().split())
        n2 = set(int(i) for i in aa[1].strip().split())
        cards[i+1] = [n1, n2, 1]

    ncards = len(cards)
    for i in range(1,ncards+1):
        mcount=0
        for c in cards[i][1]:
            if c in cards[i][0]:
                mcount +=1
        for a in range(i+1, i+mcount+1):
            cards[a][2] = cards[a][2] + cards[i][2]

    sum = 0
    for c in cards:
        sum += cards[c][2]
    print('Part2', sum)

part1()
part2()