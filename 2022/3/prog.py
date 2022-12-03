import sys 

def part1():
    score = 0
    with open(sys.argv[1]) as f:
        for line in f:
            l = line.strip()
            p1 = l[0:int(len(l)/2)]
            p2 = l[int(len(l)/2):]
            set1 = set()
            for c in p1:
                set1.add(c)
            set2 = set()
            for c in p2:
                set2.add(c)
            inter = set1.intersection(set2)
            for c in inter:
                if str(c).isupper():
                    score+= 27+ord(c)-ord('A')
                else:
                    score+= 1+ord(c)-ord('a')

    print ("Part1", score)

def part2():
    score = 0
    with open(sys.argv[1]) as f:
        idx = 0
        sets = [set(), set(), set()]
        for line in f:
            l = line.strip()
            for c in l:
                sets[idx].add(c)
            idx += 1
            if idx == 3:
                idx = 0
                inter = sets[0].intersection(sets[1].intersection(sets[2]))

                sets = [set(), set(), set()]
                assert(len(inter) == 1)

                for c in inter:
                    if str(c).isupper():
                        score+= 27+ord(c)-ord('A')
                    else:
                        score+= 1+ord(c)-ord('a')
    print ("Part2",score)

part1()
part2()