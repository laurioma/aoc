import sys
import os
import itertools

def find_all_paths(graph, pathset, start, end, path, twice, twicecnt):
    #print('s',start, path)
    if start == twice:
        twicecnt += 1
    path = path + [start]
    if start == end:
        pathset.add(''.join(path))
        return
    if not start in graph:
        return
    paths = []
    for node in graph[start]:
        if node not in path or node.isupper() or (node == twice and twicecnt < 2):
            find_all_paths(graph, pathset, node, end, path, twice, twicecnt)

def run(part2):
    lines = open(sys.argv[1]).read().splitlines()
    #print(chunks)
    graph = {}
    for l in lines:
        split = l.split('-')
        if not split[0] in graph:
            graph[split[0]] = [] 
        graph[split[0]].append(split[1])
        if not split[1] in graph:
            graph[split[1]] = []
        graph[split[1]].append(split[0])
#    print(graph)

    pathset = set()
    if not part2:
        path = []
        find_all_paths(graph, pathset, 'start', 'end', path, '', 0)
        answ = len(pathset)
    else:
        keys = list(graph.keys())
        keys.remove('start')
        keys.remove('end')
        for k in keys:
            path = []
            find_all_paths(graph, pathset, 'start', 'end', path, k, 0)

#    for pp in pathset:
#        print(pp)
    print("Part"+ ("2" if part2 else "1"), len(pathset))

run(0) if len(sys.argv) < 3 or sys.argv[2] == "1" else run(1)