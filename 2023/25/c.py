import networkx as nx
import sys

def part1():
    lines = open(sys.argv[1]).read().splitlines()
    G = nx.Graph()
    for l in lines:
        ll = l.split(':')
        for conn in ll[1].split():
            G.add_edge(ll[0], conn)

    communities = nx.community.greedy_modularity_communities(G, cutoff=2, best_n=2)
    cnt_conn = 0
    for n1 in communities[0]:
        for n2 in communities[1]:
            if G.has_edge(n1, n2):
                cnt_conn += 1
    assert(cnt_conn == 3)
    print("Part1", len(communities[0])*len(communities[1]))

part1()