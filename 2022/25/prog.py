import sys

CHARS = ['2', '1', '0', '-', '=']
VALUES = [2, 1, 0, -1, -2]

def snafu_to_dec(line):
    ret = 0
    for i in range(len(line)-1, -1,-1):
        ch = line[len(line)-1-i]
        ret += pow(5, i) * VALUES[CHARS.index(ch)]
    return ret

def dec_to_snafu(number):
    ret =''
    i=0
    while True:
        for j in range(len(VALUES)):
            chk = pow(5, i) * VALUES[j]
            if (number-chk) % pow(5, i+1) == 0:
                ret = CHARS[j] + ret
                number -= chk
                assert(number >=0)
                if number == 0:
                    return ret
                else:
                    break
        i+=1

def run():
    lines = open(sys.argv[1]).read().splitlines()
    sum = 0
    for l in lines:
        sum += snafu_to_dec(l)
    print("Part1",  dec_to_snafu(sum))

run()

