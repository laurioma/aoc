import sys 

def do(nums):
    next=[]
    allz = True
    for n in range(1, len(nums)):
        nn = nums[n] - nums[n-1]
        if nn != 0:
            allz = False
        next.append(nn)

    return next, allz

def run():
    lines = open(sys.argv[1]).read().splitlines()
    nums = []
    for l in lines:
        nums.append([int(x) for x in l.split()])

    sum1 = 0
    sum2 = 0
    for n in nums:
        first = []
        while True:
            sum1 += n[-1]
            first.append(n[0])
            next, allz = do(n)
            n = next
            if allz:
                break

        pred2 = 0
        for n in reversed(first):
            pred2 = n - pred2
        sum2 += pred2

    print('Part1', sum1)
    print('Part2', sum2)

run()
