import sys

HUMAN = 'humn'
ROOT = 'root'

def calc(tree, node):
    if not isinstance(tree[node], list):
        return tree[node]
    else:
        op = tree[node][2]
        arg1 = tree[node][0]
        arg2 = tree[node][1]
        if op == '+':
            return calc(tree, arg1) + calc(tree, arg2)
        elif op == '-':
            return calc(tree, arg1) - calc(tree, arg2)
        elif op == '*':
            return calc(tree, arg1) * calc(tree, arg2)
        else:
            assert(op == '/')
            return calc(tree, arg1) / calc(tree, arg2)

def has_humn(tree, node):
    if not isinstance(tree[node], list):
        return node == HUMAN
    else:
        return has_humn(tree, tree[node][0]) or  has_humn(tree, tree[node][1])

# climb up in tree from hmn node to root
def calc2(tree, reverse, rnode, endv):
    if not isinstance(tree[rnode], list) and not rnode == HUMAN:
        return tree[rnode]
    else:
        dst=reverse[rnode]
        if dst == ROOT:
            return endv
        op = tree[dst][2]
        arg1 = dst
        inv_order = tree[dst][1] == rnode
        arg2 = tree[dst][0] if inv_order else tree[dst][1]

        arg2v=0
        if isinstance(tree[arg2], list):
            # if 2nd argument is subtree then go and evaluate it
            arg2v = calc(tree, arg2)
        else:
            arg2v = tree[arg2]

        if op == '+':
            ret = calc2(tree,reverse, arg1, endv) 
            return ret - arg2v
        elif op == '-':
            ret = calc2(tree,reverse, arg1, endv) 
            if inv_order:
                return arg2v - ret
            else:
                return ret + arg2v
        elif op == '*':
            ret = calc2(tree,reverse, arg1, endv)
            return ret / arg2v
        else:
            assert(op == '/')
            ret =  calc2(tree,reverse, arg1, endv)
            
            if inv_order:
                return  arg2v / ret
            else:
                return ret * arg2v

def run():
    lines = open(sys.argv[1]).read().splitlines()
    tree = {}
    reverse={}
    for line in lines:
        l1 = line.split(": ")
#        print (l1, len(l1[1]))
        if len(l1[1]) <= 3:
            tree[l1[0]] = int(l1[1])
        else:
            tree[l1[0]] = [l1[1][0:4], l1[1][7:], l1[1][5]]
            reverse[l1[1][0:4]] = l1[0]
            reverse[l1[1][7:]] = l1[0]

    ret = calc(tree, ROOT)
    print("Part1", int(ret))

    side1 = tree[ROOT][0]
    side2 = tree[ROOT][1]

    inhuman_side = side2 if has_humn(tree, side1) else side1
    side_answ = calc(tree, inhuman_side)

    r = calc2(tree, reverse, HUMAN, side_answ)
    print("Part2", int(r))

run()

