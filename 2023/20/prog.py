import sys 
import re
from collections import defaultdict
from collections import deque
from math import lcm

def parse():
    lines = open(sys.argv[1]).read().splitlines()
    schema = defaultdict(lambda:['', set(), []]) # type, inputs, outputs
    for line in lines:
        ll = line.split(' -> ')
        targets = [t for t in ll[1].split(', ')]
        name = ll[0] if ll[0] in ['broadcaster'] else ll[0][1:]
        schema[name][0] = ll[0][0]# type
        for t in targets:
            schema[t][1].add(name)
        schema[name][2] = targets
    return schema

def step(schema, state, mon):
    pulses = deque([('button', 'broadcaster', False)])
    lowpulses = 0
    highpulses = 0
    monlow = set()
    while pulses:
        sender, node, pulse = pulses.popleft()
        if node in mon and not pulse:
            monlow.add(node)
        if pulse:
            highpulses += 1
        else:
            lowpulses += 1
        type, inputs, outputs = schema[node]
#        print('pulse', sender, node, dsts, pulse)

        # calc state and output
        skipupdate = False
        if node == 'broadcaster':
            outp = False
        elif type =='%':
            if not pulse:
                s = state[node]
                state[node] = not s
                outp = not s
            else:
                skipupdate = True
        elif type == '&':
            state[sender] = pulse
            iand = True
            for i in inputs:
                iv = state[i]
#                print('ands', iv)
                if not iv:
                    iand = False
                    break
            outp = not iand
            # if node in mon:
            #     print('out', outp)
        if not skipupdate:
            for ndst in outputs:
                if ndst == 'rx' and outp == False:
                    print('rx got it!')
                    return True, 0, 0
                # print(node, '->', ndst, outp)
                pulses.append((node, ndst, outp))

    return highpulses, lowpulses, monlow

def part1():
    schema = parse()

    highs = 0
    lows = 0
    state = defaultdict(lambda:False)
    for _ in range(1000):
        high, low, _ = step(schema, state, {})
        highs += high
        lows += low
    print('Part1', highs*lows)

def part2():
    schema = parse()

    inp1 = list(schema['rx'][1])
    # assuming rx is connected to 1 & gate
    assert(len(inp1) == 1 and schema[inp1[0]][0] == '&')
    # assuming this and gate is connected to several other & gates
    for i in schema[inp1[0]][1]:
        assert(schema[i][0] == '&')
    # monitor the inputs of those gates, expecting they get 'low' input periodically
    monitor = schema[inp1[0]][1]

    state = defaultdict(lambda:False)
    lowcyc = defaultdict(int)
    lowper = defaultdict(int)
    cycle = 1
    while True:
        _, _, monlow = step(schema, state, monitor)
        for m in monlow:
            if lowper[m]:
                assert(lowper[m] == cycle - lowcyc[m])
            lowper[m] = cycle - lowcyc[m]
            lowcyc[m] = cycle

        if len(lowper) == len(monitor):
            print('Part2', lcm(*lowper.values()))
            break
        cycle += 1


part1()
part2()