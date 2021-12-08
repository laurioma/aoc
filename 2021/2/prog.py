import sys 

def part1():
    depth = 0
    forward = 0
    with open(sys.argv[1]) as f:
        for line in f:
            tokens = line.split()
            print(tokens)
            if tokens[0] == "forward":
                forward += int(tokens[1])
            if tokens[0] == "up":
                depth -= int(tokens[1])
            if tokens[0] == "down":
                depth += int(tokens[1])
        print(depth, forward, depth * forward)
                
def part2():
    depth = 0
    forward = 0
    aim = 0
    with open(sys.argv[1]) as f:
        for line in f:
            tokens = line.split()
            print(tokens)
            if tokens[0] == "forward":
                forward += int(tokens[1])
                depth += int(tokens[1]) * aim
            if tokens[0] == "up":
                aim -= int(tokens[1])
            if tokens[0] == "down":
                aim += int(tokens[1])
        print(depth, forward, depth * forward)

part1() if len(sys.argv) < 3 or sys.argv[2] == "1" else part2()
