import sys 

def run():
    sum = 0
    sums = []
    with open(sys.argv[1]) as f:
        for line in f:
            if line.strip() != "":
                cal = int(line)
                sum += cal
            else:
                sums.append(sum)
                sum = 0
    sums.sort(reverse=True)
    print("Part1", sums[0])
    print("Part2", sums[0]+sums[1]+sums[2])

run()