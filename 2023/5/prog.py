import sys 

def parse():
    lines = open(sys.argv[1]).read().splitlines()
    seeds = [int(x) for x in lines[0].split(':')[1].split()]

    maps = []
    map = []
    for line in lines[3:]:
        if line == '':
            maps.append(map)
            map = []
            continue
        if not line[0].isdigit():
            continue
        vals = [int(x) for x in line.split()]
        map.append((vals[1], vals[0], vals[2]))

    maps.append(map)
    return seeds, maps

def part1():
    seeds, maps = parse()
    minloc = sys.maxsize 
    for i,s in enumerate(seeds):
        key = s
        for i,map in enumerate(maps):
            v = key
            for me in map:
                if me[0] <= v and (me[0] + me[2]) > v:
                    v = me[1] + v - me[0]
                    break

            key = v
        if v < minloc:
            minloc = v

    print('Part1', minloc)

def map_range(range_in, map):
    rng_out = []
    in_start, in_stop = range_in
    for m in map:
        map_in_start = m[0]
        map_in_stop = m[0] + m[2] - 1
        offset = m[1] - m[0]
        # non mapped before start
        if in_start < map_in_start:
            if in_stop < map_in_start:
                rng_out.append((in_start, in_stop))
                return rng_out
            else:
                rng_out.append((in_start, map_in_start - 1))
                in_start = map_in_start
        # overlapping part
        if in_start >= map_in_start and in_start <= map_in_stop:
            if in_stop >= map_in_stop:
                rng_out.append((in_start + offset, map_in_stop + offset))
                in_start = map_in_stop+1
            else:
                rng_out.append((in_start + offset, in_stop + offset))
                return rng_out
    # non mapped after last stop
    if in_stop > map_in_stop:
        rng_out.append((in_start, in_stop))
    return rng_out
            
def part2():
    seeds1, maps = parse()
    seeds=[]
    for i in range(0, len(seeds1), 2):
        seeds.append((seeds1[i], seeds1[i] + seeds1[i+1] - 1))
    for i in range(len(maps)):
        maps[i] = sorted(maps[i], key=lambda x: x[0])

    minloc = sys.maxsize 
    for i,s in enumerate(seeds):
        rng_in = [s]
        for i,map in enumerate(maps):
            mapped_rng = []
            for rin in rng_in:
                mapped_rng += map_range(rin, map)
            rng_in = mapped_rng
        for r in mapped_rng:
            if r[0] < minloc:
                minloc = r[0]

    print('Part2', minloc)

part1()
part2()