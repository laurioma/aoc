import sys
import itertools

def decode_packet(s, versions):
    ver = int(s[0:3], 2)
    type = int(s[3:6], 2)
    versions.append(ver)
#    print("decode", ver, type, s)
    if type == 4:
        bins1 = s[6:]
#        print("bins", bins1)
        binn = ""
        litlen_bit = 6
        while True:
            litlen_bit += 5
            binn += bins1[1:5]
#            print("bin", binn, bins1, int(binn[1:], 2))
            if bins1[0] == "0":
                break
            bins1 = bins1[5:]
        return (litlen_bit, type, int(binn, 2), [])
    else:
        lenid = s[6]
#        print("operator", lenid, s)
        if lenid == "0":
            plen = int(s[7:22], 2)
#            print("op0 len", plen, bin(plen))
            start = 22
            remaining = plen
            subs = []
            while remaining > 6:
                sub = decode_packet(s[start:start+remaining], versions)
                subs.append(sub)
                remaining -= sub[0]
                start += sub[0]
#            print("plen", plen, remaining)
            return (22 + plen, type, 0,  subs) 
        else:
            numsub = int(s[7:18], 2) 
#            print("op1 numsub", numsub, bin(numsub))
            start = 18
            subs = []
            for i in range(numsub):
               sub = decode_packet(s[start:], versions)
               subs.append(sub)
               start += sub[0]
            return (start, type, -1, subs)

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
#        print("bins", bins)
        versions = []
        packets = decode_packet(bins, versions)
#        print(versions, sum(versions), packets)

        print("Part1", sum(versions))

        print("Part2", calculate(packets))

        
run()