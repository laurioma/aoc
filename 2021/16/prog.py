import sys
import itertools

def read_bits(s, num):
    bins = s[0:num]
    return (int(bins, 2), s[num:])

def decode_packet(s, versions):
    startlen = len(s)
    ver, s = read_bits(s, 3)
    type, s = read_bits(s, 3)
    value = 0
    subs = []
    versions.append(ver)
    if type == 4:
        while True:
            cont, s = read_bits(s, 1)
            v, s = read_bits(s, 4)
            value = (value << 4) + v
            if cont == 0:
                break
    else:
        lenid, s = read_bits(s, 1)
        if lenid == 0:
            plen, s = read_bits(s, 15)
            remaining = plen

            while remaining > 6:
                sub = decode_packet(s, versions)
                s = s[sub[0]:]
                subs.append(sub)
                remaining -= sub[0]
        else:
            numsub, s = read_bits(s, 11)
            for i in range(numsub):
               sub = decode_packet(s, versions)
               s = s[sub[0]:]
               subs.append(sub)
    
    return (startlen - len(s), type, value, subs)

def calculate(packets):
    #value
    if packets[1] == 4:
        return packets[2]
    elif packets[1] == 0:
        sum = 0
        for sp in packets[3]:
            sum += calculate(sp)
        return sum
    elif packets[1] == 1:
        prod = 1
        for sp in packets[3]:
            prod *= calculate(sp)
        return prod
    elif packets[1] == 2:
        val = []
        for sp in packets[3]:
            val.append(calculate(sp))
        return min(val)
    elif packets[1] == 3:
        val = []
        for sp in packets[3]:
            val.append(calculate(sp))
        return max(val)    
    elif packets[1] == 5:
        sp1 = calculate(packets[3][0])
        sp2 = calculate(packets[3][1])
        return 1 if sp1 > sp2 else 0
    elif packets[1] == 6:
        sp1 = calculate(packets[3][0])
        sp2 = calculate(packets[3][1])
        return 1 if sp1 < sp2 else 0
    elif packets[1] == 7:
        sp1 = calculate(packets[3][0])
        sp2 = calculate(packets[3][1])
        return 1 if sp1 == sp2 else 0

def run():
    lines = open(sys.argv[1]).read().splitlines()
    for l in lines:
        s = l.strip()
        intv = int(s,16)
        lenhex = len(s)
        bins = format(intv, '0'+str(lenhex*4)+'b')
        versions = []
        packets = decode_packet(bins, versions)

        print("Part1", sum(versions))

        print("Part2", calculate(packets))

        
run()