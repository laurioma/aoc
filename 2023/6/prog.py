import sys 

def part1():
    lines = open(sys.argv[1]).read().splitlines()
    times = [int(t) for t in lines[0].split(':')[1].split()]
    distances = [int(t) for t in lines[1].split(':')[1].split()]

    score = 1
    for i in range(len(distances)):
        count = 0
        record = distances[i]
        for hold in range(times[i]):
            time = times[i] - hold
            speed = hold
            dist = time * speed
            if dist > record:
                count += 1
        score *= count

    print('Part1', score)

def part2():
    # times = [71530]
    # distances = [940200]    
    times = [49877895]
    distances = [356137815021882]
    score = 1
    for i in range(len(distances)):
        count = 0
        record = distances[i]
        for hold in range(times[i]):
            time = times[i] - hold
            speed = hold
            dist = time * speed
            if dist > record:
                count += 1
        score *= count

    print('Part2', score)

part1()
part2()