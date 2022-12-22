import sys
import re
import collections as ct
import math
import sympy

def has_humn(tree, node):
    if not isinstance(tree[node], list):
        return node == 'humn'
    else:
        return has_humn(tree, tree[node][0]) or  has_humn(tree, tree[node][1])

def calcs(tree, node, xnode):
    if node == xnode:
        return sympy.Symbol('x')
    elif not isinstance(tree[node], list):
        return sympy.Integer(tree[node])
    else:
        op = tree[node][2]
        arg1 = tree[node][0]
        arg2 = tree[node][1]
        if op == '+':
            return calcs(tree, arg1, xnode) + calcs(tree, arg2, xnode)
        elif op == '-':
            return calcs(tree, arg1, xnode) - calcs(tree, arg2, xnode)
        elif op == '*':
            return calcs(tree, arg1, xnode) * calcs(tree, arg2, xnode)
        else:
            assert(op == '/')
            return calcs(tree, arg1, xnode) / calcs(tree, arg2, xnode)

def part1():
    lines = open(sys.argv[1]).read().splitlines()
    tree = {}
    for line in lines:
        l1 = line.split(": ")
        if len(l1[1]) <= 3:
            tree[l1[0]] = float(l1[1])
        else:
            tree[l1[0]] = [l1[1][0:4], l1[1][7:], l1[1][5]]

    ret = calcs(tree, 'root', None)
    print("Part1", ret)

    side1 = tree['root'][0]
    side2 = tree['root'][1]

    human_side = side1 if has_humn(tree, side1) else side2
    nonhuman_side = side2 if has_humn(tree, side1) else side1
    side_answ = calcs(tree, nonhuman_side, None)
    sym_res = calcs(tree, human_side, 'humn')

    print("Part2", sympy.solve(sym_res - sympy.Integer(side_answ))[0])

part1()

