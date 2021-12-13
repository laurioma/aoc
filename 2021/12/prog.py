import sys

def find_all_paths(graph, start, end, path, part2, twice):
#    print('s',start, twice, path.count(start), path)
    if part2 and twice == '' and start.islower() and path.count(start) == 1:
        twice = start
    path = path + [start]
    if start == end:
        return 1
    if not start in graph:
        return 0

    count = 0
    for node in graph[start]:
        if node not in path or node.isupper() or (part2 and node != 'start' and twice == ''):
            count += find_all_paths(graph, node, end, path, part2, twice)
    return count

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
    path = []

    count = find_all_paths(graph, 'start', 'end', path,  part2, '')

#    for pp in pathset:
#        print(pp)
    print("Part"+ ("2" if part2 else "1"), count)

run(0) if len(sys.argv) < 3 or sys.argv[2] == "1" else run(1)