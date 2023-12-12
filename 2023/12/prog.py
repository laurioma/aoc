import sys 

def count_placements(cache, springs, groups, sidx=0, gidx=0, lvl=0):
    if gidx >= len(groups):
        # check if remaining part has no #
        if springs[sidx:].count('#') == 0:
            return 1
        else:
            return 0

    key = str(gidx) + str(sidx)
    if cache != None:
        if key in cache:
            return cache[key]

#    print(lvl, ''.join(springs), groups, sidx, gidx, len(groups), groups[gidx:], 'rem', ''.join(springs[sidx:]))

    count = 0
    glen = groups[gidx]    
    i = sidx
    while True:
        if i + glen > len(springs):
            break
        # don't step over '#'
        if i > 0 and springs[i-1] == '#':
            break

        # check if group fits and has no # following it
        if springs[i:i+glen].count('.') == 0 and (i + glen == len(springs) or (springs[i + glen] in '.?')):
            nex_springs = springs[:]

            if i + glen < len(springs) and nex_springs[i + glen] == '?':
                nex_springs[i + glen] = '.'

            for x in range(i,i+glen):
                nex_springs[x] = '#'

            count += count_placements(cache, nex_springs, groups, i + glen + 1, gidx + 1, lvl+1)
        i += 1

    if cache != None:
        cache[key] = count
    return count

def part1():
    lines = open(sys.argv[1]).read().splitlines()
    sum = 0
    for l in lines:
        ll = l.split()
        springs = list(ll[0])
        configs = [int(c) for c in ll[1].split(',')]

        ret = count_placements(None, springs, configs)
        sum += ret

    print('Part1', sum)

def part2():
    lines = open(sys.argv[1]).read().splitlines()
    sum = 0
    for li, l in enumerate(lines):
        springs, configs = l.split()
        configs = [int(c) for c in configs.split(',')]
        springs1 = ''
        configs1 = []
        for i in range(5):
            springs1 += ('?' if i != 0 else '') + springs
            configs1 += configs

#        print("s   ", springs1, configs1, li)
        cache = {}
        cnt = count_placements(cache, list(springs1), configs1)
#        print("    ", springs1, configs1, cnt)

        sum += cnt

    print('Part2', sum)

part1()
part2()

