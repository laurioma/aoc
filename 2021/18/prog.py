import sys
import itertools
import re
import json

def add_pairs(a, b):
    return [a, b]

def run_explode(s, idx):
    idxr = s.find(']', idx)
    pairs = s[idx:idxr+1]
    pair = eval(pairs)
    firsthalf = s[0:idx]
    sechalf = s[idxr+1:]

    m = re.search('(\d+)(?!.*\d)', firsthalf) # last number
    if m:
        firstn = m.group()
        firsthalf = re.sub("(\d+)(?!.*\d)", str(int(firstn)+ pair[0]), firsthalf, 1)
    m = re.search('[0-9]+', sechalf)
    if m:
        secn = m.group()
        sechalf = re.sub("[0-9]+", str(int(secn)+ pair[1]), sechalf, 1)
    s = firsthalf + "0"+ sechalf

    return s, pair

def explode(s):
    # print ("expl in", s)
    count_open = 0
    for i in range(len(s)):
        if s[i] == "[":
            count_open += 1
        if s[i] == "]":
            count_open -= 1
        if count_open == 5:
            ret =  run_explode(s, i)
            # print("expl EX", ret[0], ret[1])
            return ret[0], True
    # print("expl noexplode")
    return s, False

def run_split(a):
    if not isinstance(a, list):
        if a > 9:
            return [int(a/2), int(a/2) + a%2], True
        else:
            return a, False
    else:
        v1, spl = run_split(a[0])
        if spl:
            return [v1, a[1]], True
        v2, spl = run_split(a[1])
        if spl:
            return [a[0], v2], True
        return [v1, v2], False

def run_explode_split(expr):
    exprs = json.dumps(expr)
    while True:
        exprs, exploded = explode(exprs)
        if exploded:
            continue

        expr = eval(exprs)
        # print("b4 split", expr)
        expr, splitted = run_split(expr)
        # print("af split", expr)
        if not splitted:
            break
        else:
            exprs = json.dumps(expr)
    return expr

def mag(a):
    left = right = -1
    if not isinstance(a[0], list) :
        left = a[0]
    else:
        left = mag(a[0])
    if not isinstance(a[1], list) :
        right = a[1]
    else:
        right = mag(a[1])
    return (left * 3 +  right * 2)

def run():
    lines = open(sys.argv[1]).read().splitlines()
    first = True
    for l in lines:
        if first:
            expr = eval(l)
            first = False
        else:
            add = eval(l)
            expr = add_pairs(expr, add)        
            expr = run_explode_split(expr)

    print("Part1", mag(expr))

    maxmag = 0
    exprs = []
    for l in lines:
        exprs.append(eval(l))

    for i, j in itertools.product(range(len(exprs)), range(len(exprs))):
        if i == j:
            continue
        e = add_pairs(exprs[i], exprs[j])        
        e = run_explode_split(e)
        m = mag(e)
        if m > maxmag:
            maxmag = m

    print("Part2", maxmag)

run()
