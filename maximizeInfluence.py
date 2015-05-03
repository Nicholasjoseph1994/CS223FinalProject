import random
import math
import numpy as np
from collections import Counter

"""
eps is precision parameter between 0 and 1
G is a directed edge weighted graph
n is the number of vertices
m is the number of edges
"""
def maximizeInfluence(eps, Gt, n, m, k):
    R = int(144 * n * m * math.log(n) / (float(eps)**3))
    print R
    H = buildHyperGraph(R, Gt, n, m)
#    print H
    return buildSeedSet(H, k, n)

"""
R is the number of steps to take before terminating
G is a directed edge weighted graph
"""
def buildHyperGraph(R, Gt, n, m):
    #H is a list of lists of sets, h[n][i] is the ith edge that n is in (edges are sets)
    H = [[] for _ in xrange(n)]
    counter = 0
    while counter < R:
        u = random.randrange(n)
        Z = simulateSpread(Gt, u)
        for n2 in Z:
            H[n2].append(Z)
        counter += len(Z)
    return H

"""
Gt is the transpose of the graph
u is the starting node
returns the set of all nodes discovered
"""
def simulateSpread(Gt, u):
    V = set([u])
    stack = [u]
    while len(stack):
        n = stack.pop()
        for nextVertex in Gt[n]:
            n2 = nextVertex[0]
            if random.random() < nextVertex[1] and n2 not in V:
                stack.append(n2)
                V.add(n2)
    return V

def correctHead (head, setsByDegree):
    while len(setsByDegree[head]) == 0:
        head -= 1
    return head

"""
H is a hypergraph represented as a set of vertices and a set of sets of vertices
k is the number of seed nodes
"""
def buildSeedSet(H, k, n):
    # initialize
    verticesByDegree = [set() for _ in xrange(n)]
    head = -1
    for node, edges in enumerate(H):
        print len(edges)
        verticesByDegree[len(edges)].add(node)

    vk = []
    for _ in xrange(k):
        head = correctHead(head, verticesByDegree)
        minVertex = verticesByDegree[head].pop()
        vk.append(minVertex)
        for edge in H[minVertex]:
            for n in edge:
                deg = len(H[n])
                H[n].remove(edge)
                verticesByDegree[deg].remove(n)
                verticesByDegree[deg-1].add(n)

    return vk

def uniformize(G, p):
    for node, edges in enumerate(G):
        G[node] = [(i, p) for i in edges]
    return G

def transpose(G, n):
    G2 = [[] for _ in xrange(n)]

    for n, edges in enumerate(G):
        for n2 in edges:
            G2[n2].append(n)

    return G2

def test1():
    G = []
    G.append([1, 2])
    G.append([3, 4])
    G.append([5, 6])
    G.append([])
    G.append([])
    G.append([])
    G.append([])

    G.append([8, 9])
    G.append([10, 11])
    G.append([12, 13])
    G.append([])
    G.append([])
    G.append([])
    G.append([])


    G = uniformize(transpose(G), .5)

    print maximizeInfluence(.5, G, 14, 12, 2)

if __name__ == '__main__':
    test1()
