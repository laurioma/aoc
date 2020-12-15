import sys
import time
import re
import copy

def find_last(nums, last, array_len):
    if last in nums:
        return array_len - nums[last]
    else:
        return 0

def execute(file, part2):
    with open(file) as f:
        lines = f.readlines()

    print(lines)
    nums = dict()
    last = 0
    prelast = -1
    idx = 0
    for n in lines[0].split(","):
        if prelast != -1:
            nums[last] = idx
        prelast = last
        last = int(n)
        idx+=1
    print(nums)

    max = 2020
    if part2:
        max = 30000000

    for turn in range(max - idx):
#        print ("find last", last, idx)
        newlast = find_last(nums, last, idx)
#        print ("newlast", newlast)
        nums[last]=idx
        last = newlast
        idx += 1
    
#    print(nums)
    print("answer", last, "len", idx)

execute(sys.argv[1], int(sys.argv[2]))