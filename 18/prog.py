import sys
import time
import copy
import re

def calculate(expr):
    value = 0
    i = 0
    while i < len(expr):
#        print ("CALC", i, expr[i], isinstance(expr[i], int), isinstance(expr[i], str), isinstance(expr[i],list))
        if i == 0:
            if isinstance(expr[i], list):
                value = calculate(expr[i])
            else:
                assert(isinstance(expr[i], int))
                value = expr[i]
            i+=1
        else:
            if isinstance(expr[i], str):
                if isinstance(expr[i + 1], int):
                    if expr[i] == '+':
                        value += expr[i + 1]
                    elif expr[i] == '*':
                        value *= expr[i + 1]
                    else:
                        assert(False)
                else:
                    assert(isinstance(expr[i + 1], list))
                    val2 = calculate(expr[i + 1])
                    if expr[i] == '+':
                        value += val2
                    elif expr[i] == '*':
                        value *= val2
                    else:
                        assert(False)
                i += 2
            else:
                assert(False)
    return value

def prioritizeadd(expr):
    i = 0
    while i < len(expr):
        if isinstance(expr[i], list):
            prioritizeadd(expr[i])

        if expr[i] == '+':
            o1 = expr[i - 1]
            o2 = expr[i + 1]
            if isinstance(o2, list):
                prioritizeadd(o2)
            del(expr[i-1:i+1])
            expr[i-1] = [o1, '+', o2]
        else:
            i+=1


#2 * 3 + (4 * 5)
def execute(file, part2):

    answer = 0
    with open(file) as f:
        for line in f:
            expr = []
            inslist = expr
            stack = []
            for i in range(len(line.rstrip())):
#                print (line[i])
                m = re.search("\d+", line[i]) 
                if m:
                    inslist.append(int(m.group(0)))
                else:
                    m = re.search("[+*]", line[i]) 
                    if m:
                        inslist.append(m.group(0))
                    elif line[i] == "(":
                        newl = []
                        inslist.append(newl)
                        stack.append(inslist)
                        inslist = newl
                    elif line[i] == ")":
                        inslist = stack.pop()
                    else:
                        if line[i] != ' ':
                            print("???",line[i],'+')
                            assert(False)
            print(expr)
            if part2:
                prioritizeadd(expr)
                print("add++", expr)
            res = calculate(expr)
            print(expr, "=", res)
            answer += res

    print ("Result", answer)

execute(sys.argv[1], int(sys.argv[2]))


