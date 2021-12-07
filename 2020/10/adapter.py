import sys 

adapters = []
max_val = 0
with open(sys.argv[1]) as f:
    for line in f:
        if max_val < int(line):
            max_val = int(line)
        adapters.append(int(line))

adapters.append(0)
adapters.append(max_val + 3)

adapters.sort()

print("adapters:", adapters)

diffs = dict()
for i in range(1,len(adapters)):
    diff = adapters[i] - adapters[i-1]
    diffs[diff] = diffs.get(diff, 0) + 1
    
print ("DIFFS:", diffs)
print("answer p1:", diffs.get(1, 0) * diffs.get(3, 0))

variants = 1
subvar = 1
can_remove_cnt = 0
for i in range(1,len(adapters)-1):
    diff1 = adapters[i] - adapters[i-1]
    diff2 = adapters[i+1] - adapters[i]
    if (diff1 == 1 and diff2 == 1):
        can_remove_cnt += 1
        subvar *= 2
        if can_remove_cnt > 2:
            subvar -= (can_remove_cnt-2)
            print("reduce subvar ", subvar)      
        print("can remove i", i , "a", adapters[i], "d1", diff1, "d2", diff2, "subvar", subvar, "can_remove_cnt ", can_remove_cnt)            
    else:
        variants *= subvar
        print("group end", variants , "subvar", subvar)            
        subvar = 1
        can_remove_cnt = 0
print("answer p2", variants)



