import sys
import os
import itertools

def find_all_paths(graph, start, end, path=[]):
    #print('s',start, path)
    path = path + [start]
    if start == end:
        return [path]
    if not start in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path or node.isupper():
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def find_all_paths2(graph, start, end, path, twice, twicecnt):
    #print('s',start, path)
    if start == twice:
        twicecnt += 1
    path = path + [start]
    if start == end:
        return [path]
    if not start in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path or node.isupper() or (node == twice and twicecnt < 2):
            newpaths = find_all_paths2(graph, node, end, path, twice, twicecnt)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def run(part2):
    with open(sys.argv[1]) as f:
        data = f.read()
    chunks = data.split('\n')
    print(chunks)
    graph = {}
    for c in chunks:
        split = c.split('-')
        if not split[0] in graph:
            graph[split[0]] = [] 
        graph[split[0]].append(split[1])
        if not split[1] in graph:
            graph[split[1]] = []
        graph[split[1]].append(split[0])
    print(graph)

    path = []
    p = []
    if not part2:
        p = find_all_paths(graph, 'start', 'end', path)
    else:
        keys = list(graph.keys())
        keys.remove('start')
        keys.remove('end')
        for k in keys:
            path = []
            pp = find_all_paths2(graph, 'start', 'end', path, k, 0)
            for ppp in pp:
                if ppp not in p:
                    p.append(ppp)
 #   for pp in p:
 #       print(pp)
    print(len(p))

run(len(sys.argv)>=3)