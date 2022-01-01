import sys
import itertools
import asyncio

OP_ADD      = 1
OP_MUL      = 2
OP_IN       = 3
OP_OUT      = 4
OP_JMPT     = 5
OP_JMPF     = 6
OP_LESS     = 7
OP_EQ       = 8
OP_END      = 99

PMODE_POS   = 0
PMODE_IMM   = 1


def getp(prog, pos, pidx):
    pmode = int(prog[pos] % 1000 / 100)
    if pidx == 2:
        pmode = int(prog[pos] % 10000 / 1000)

    if pmode == PMODE_IMM:
        return prog[pos+pidx]
    else:
        return prog[prog[pos+pidx]]

async def run_prog(idx, prog_in, readq, writeq):
    pos = 0
    prog = prog_in.copy()
    while True:
        op = prog[pos] % 100

        if op == OP_ADD:
            prog[prog[pos+3]] = getp(prog, pos, 1) + getp(prog, pos, 2)
            pos += 4
        elif op == OP_MUL:
            prog[prog[pos+3]] = getp(prog, pos, 1) * getp(prog, pos, 2)
            pos += 4
        elif op == OP_IN:
            # print("try read", idx)
            r = await readq.get()
            # print("read", idx, r)
            prog[prog[pos+1]] = r
            pos += 2
        elif op == OP_OUT:
            # print("write", idx, getp(prog, pos, 1))
            writeq.put_nowait(getp(prog, pos, 1))
            pos += 2
        elif op == OP_JMPT:
            if getp(prog, pos, 1) != 0:
                pos = getp(prog, pos, 2)
            else:
                pos += 3
        elif op == OP_JMPF:
            if getp(prog, pos, 1) == 0:
                pos = getp(prog, pos, 2)
            else:
                pos += 3
        elif op == OP_LESS:
            if getp(prog, pos, 1) < getp(prog, pos, 2):
                prog[prog[pos+3]] = 1
            else:
                prog[prog[pos+3]] = 0
            pos += 4
        elif op == OP_EQ:
            if getp(prog, pos, 1) == getp(prog, pos, 2):
                prog[prog[pos+3]] = 1
            else:
                prog[prog[pos+3]] = 0
            pos += 4
        elif op == OP_END:
            break
        else:
            raise Exception("invalid opcode")

MAX_AMP = 5
MAX_PHASE = 5

async def calc_amp(part2, prog):
    max = 0
    ioq = [asyncio.Queue(2) for _ in range(MAX_AMP)]
    for p in itertools.permutations(range(MAX_PHASE), MAX_AMP):
        tasks = []
        for amp in range(MAX_AMP):
            phase = p[amp] + 5 if part2 else p[amp]
            ioq[amp].put_nowait(phase)
            if amp == 0:
                ioq[0].put_nowait(0)
            nextamp = 0 if amp == MAX_AMP-1 else amp+1
            task = asyncio.create_task(run_prog(amp, prog, ioq[amp], ioq[nextamp]))
            tasks.append(task)
        await asyncio.wait(tasks)
        res = await ioq[0].get()
        if max < res:
            max = res
    return max

def run():
    progs = open(sys.argv[1]).read().split(",")
    prog = [int(p) for p in progs]
    ret = asyncio.run(calc_amp(0, prog))
    print("Part1:", ret)
    ret = asyncio.run(calc_amp(1, prog))
    print("Part2:", ret)

run()