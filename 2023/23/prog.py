import sys 
from collections import defaultdict

def printm(matrix, path=None):
    for y,r in enumerate(matrix):
        for x,c in enumerate(r):
            if path != None and (x, y) in path:
                print('O', end='')
            else:
                print(c, end='')
        print("")

def to_graph(mat, start, end, part1):
    crosses = [start, end]
    for y in range(len(mat)):
        for x in range(len(mat[0])):
            if mat[y][x] != '#':
                cnt = 0
                for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx = x + d[0]
                    ny = y + d[1]

                    if 0 <= nx < len(mat[0]) and 0 <= ny < len(mat) and mat[ny][nx] != '#':
                        cnt += 1
                if cnt > 2:
                    crosses.append((x,y))
    edges = defaultdict(list)
    for c in crosses:
        q = [(c, 1)]
        visited = set()
        while q:
            nc, dist = q.pop(0)
            visited.add(nc)

            for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx = nc[0] + d[0]
                ny = nc[1] + d[1]
                if 0 <= nx < len(mat[0]) and 0 <= ny < len(mat) and (nx, ny) not in visited and  mat[ny][nx] != '#':
                    if part1:
                        if mat[ny][nx] == '<':
                            if d != (-1, 0):
                                continue
                        if mat[ny][nx] == '>':
                            if d != (1, 0):
                                continue
                        if mat[ny][nx] == 'v':
                            if d != (0, 1):
                                continue
                    if (nx, ny) in crosses:
                        edges[c].append(((nx, ny), dist))
                    else:
                        q.append(((nx, ny), dist+1))
    return edges
    
def walkg_dfs(visited, graph, node, end, length):
    if node == end: 
        return length
    ret = 0
    if node not in visited:
        visited.add(node)
        for next, dst in graph[node]:
            r = walkg_dfs(visited, graph, next, end, length + dst)
            if r > ret:
                ret = r
        visited.remove(node)
        return ret
    return 0

def part1():
    lines = open(sys.argv[1]).read().splitlines()
    matrix = [list(row) for row in lines]; w=len(matrix[0]); h=len(matrix)

    edges = to_graph(matrix, (1,0), (w-2, h-1), True)

    visited = set()
    longest = walkg_dfs(visited, edges, (1,0), (w-2, h-1), 0)

    print('Part2', longest)

def part2():
    lines = open(sys.argv[1]).read().splitlines()
    matrix = [list(row) for row in lines]; w=len(matrix[0]); h=len(matrix)

    edges = to_graph(matrix, (1,0), (w-2, h-1), False)

    visited = set()
    longest = walkg_dfs(visited, edges, (1,0), (w-2, h-1), 0)

    print('Part2', longest)

part1()
part2()
