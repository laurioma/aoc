import sys
import re

class Monkey:
    def __init__(self, items, op, opv, div, truem, falsem):
        self.items = items
        self.op = op
        self.opv = opv
        self.div = div
        self.truem = truem
        self.falsem = falsem
        self.inspectc = 0

def read_monkey(data, monkeys):
    lines=data.splitlines()
    m = re.search('Monkey (\d+):', lines[0]);
    assert(m)
    items_s = lines[1].split(':')[1].split(',')
    items = []
    for s in items_s:
        items.append(int(s.strip()))
    m = re.search('Operation: new = old ([*+]) (.*)', lines[2]);
    assert(m)
    op = m.group(1)
    opv = m.group(2)
    m = re.search('Test: divisible by (\d+)', lines[3]);
    assert(m)
    div = int(m.group(1))
    m = re.search('If true: throw to monkey (\d+)', lines[4]);
    assert(m)
    truem = int(m.group(1))
    m = re.search('If false: throw to monkey (\d+)', lines[5]);
    assert(m)
    falsem = int(m.group(1))
    monkeys.append(Monkey(items, op, opv, div, truem, falsem))

def run(part):
    monkeys=[]
    monkeydata = open(sys.argv[1]).read().strip('\r').split('\n\n')
    for md in monkeydata:
        read_monkey(md, monkeys)

    denom = 1
    for m in monkeys:
        denom *= m.div
    max = 20
    if part == 2:
        max = 10000
    for _ in range(max):
        for (mi, m) in enumerate(monkeys):
            for _ in range(len(m.items)):
                i = m.items.pop(0)
                # print('monkey', mi, 'inspect', i)
                m.inspectc += 1
                if m.op == '*':
                    if m.opv == 'old':
                        i *= i
                    else:
                        i *= int(m.opv)
                else:
                    assert(m.op == '+')
                    if m.opv == 'old':
                        i += i
                    else:
                        i += int(m.opv)
                if part == 2:
                    i = i % denom
                else:
                    i = int(i/ 3)
                if i % m.div == 0:
                    monkeys[m.truem].items.append(i)
                else:
                    monkeys[m.falsem].items.append(i)
    inspectc = []
    for m in monkeys:
        inspectc.append(m.inspectc)
    inspectc.sort(reverse=True)
    print ('Part%d %d'%(part,inspectc[0]*inspectc[1]))


run(1)
run(2)