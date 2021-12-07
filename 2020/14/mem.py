import sys
import time
import re


with open(sys.argv[1]) as f:
    lines = f.readlines()

def get_andmask(bstr):
    mask = 0
    for i in range(len(bstr)):
        if bstr[i] != '0':
            mask += pow(2, len(bstr) - 1 - i)
    print("AND 0x{0:x}".format(mask))
    return mask

def get_ormask(bstr):
    mask = 0
    for i in range(len(bstr)):
        if bstr[i] == '1':
            mask += pow(2, len(bstr) - 1 - i)
    print("OR 0x{0:x}".format(mask))
    return mask

def apply_part1(addr, value, mem, andmask, ormask):
    value &= andmask
    value |= ormask
    print ("value andor", value)
    mem[addr] = value

def apply_part2(addr, value, mem, ormask, maskstr):
    float_cnt = maskstr.count('X')
    print ("float_cnt", float_cnt)
    for i in range(pow(2, float_cnt)):
        floataddr = 0
        tmp = i
        addr2 = (addr | ormask)
        for j in range(len(maskstr)):
            if (maskstr[len(maskstr) - 1 - j] == 'X'):
#                print ("X", j, tmp, tmp & 1)
                if (tmp & 1):
                    floataddr += pow(2, j)
#                    print ("set b {0} {1:x}", j, addr3)
                    addr2 |= pow(2, j)
                else:
#                    print ("clear b {0} {1:x}", j, addr3)
                    addr2 &= ~pow(2, j)
                
                tmp = int(tmp / 2)

#        print ("float {0} {1:x} a {2:x}({2}) WRITE {3:x}({3}) = {4}".format(i, floataddr, addr, addr2, value))
        mem[addr2] = value


def execute(part2):
    maskstr = ""
    andmask = 0
    ormask = 0
    mem = dict()
    for line in lines:
        res = re.search('mask = ([X01]+)', line)
        if (res):
            print ("res", res.group(1))
            andmask = get_andmask(res.group(1))
            ormask = get_ormask(res.group(1))
            maskstr = res.group(1)
            print ("masks and 0x{0:x} or 0x{1:x}".format(andmask, ormask))
        else:
            res = re.search('mem\[(\d+)\] = (\d+)', line)
            if (res):
                print ("instr", res.group(1), res.group(2))
                addr = int(res.group(1))
                value = int(res.group(2))
                if part2:
                    apply_part2(addr, value, mem, ormask, maskstr)
                else:
                    apply_part1(addr, value, mem, andmask, ormask)
            else:
                print("PARSE ERROR")

    result = 0
    for key in mem:
        result += mem[key]

    print ("answer p{0}: {1}".format(2 if part2 else 1, result))


execute(int(sys.argv[2]))