import sys 

def part1():
    last_depth = -1
    inc = 0
    with open(sys.argv[1]) as f:
        for line in f:
            depth = int(line)
            if last_depth != -1 and depth > last_depth:
                inc +=1
            last_depth = depth
    print(inc)

def part2():
    depths = []
    last_depth = -1
    inc = 0
    with open(sys.argv[1]) as f:
        for line in f:
            depths.append(int(line))            
            if len(depths) > 3:
                depths.pop(0)
            if len(depths) == 3:
                sum = 0
                for depth in depths:
                    sum += depth
                avgd = sum / 3
                print(sum)
                if last_depth != -1 and avgd > last_depth:
                    inc +=1
                last_depth = avgd
    print(inc)

part1() if len(sys.argv) < 3 or sys.argv[2] == "1" else part2()
