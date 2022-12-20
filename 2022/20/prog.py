import sys
import re

def mix_array(arr):
    for i in range(len(arr)):
        (n, pos) = next((arr[j], j) for j in range(len(arr)) if arr[j][0] == i)
        arr.pop(pos)
        newpos = (pos + n[1]) % len(arr)
        arr.insert(newpos, n)

def part1():
    lines = open(sys.argv[1]).read().splitlines()
    arr = list((i, int(lines[i])) for i in range(len(lines)))

    mix_array(arr)

    zpos = next(j for j in range(len(arr)) if arr[j][1] == 0)
    pos1000=(zpos + 1000) % len(arr)
    pos2000=(zpos + 2000) % len(arr)
    pos3000=(zpos + 3000) % len(arr)
    print("Part1", arr[pos1000][1]+arr[pos2000][1]+arr[pos3000][1])

def part2():
    lines = open(sys.argv[1]).read().splitlines()
    arr = list((i, int(lines[i])) for i in range(len(lines)))

    key= 811589153
    for i in range(len(arr)):
        arr[i] = (arr[i][0], arr[i][1]*key)

    for _ in range(10):
        mix_array(arr)

    zpos = next(j for j in range(len(arr)) if arr[j][1] == 0)
    pos1000=(zpos + 1000) % len(arr)
    pos2000=(zpos + 2000) % len(arr)
    pos3000=(zpos + 3000) % len(arr)
    print("Part2", arr[pos1000][1]+arr[pos2000][1]+arr[pos3000][1])

part1()
part2()


