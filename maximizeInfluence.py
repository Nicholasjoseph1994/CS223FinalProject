import random
import math
from collections import Counter

"""
eps is precision parameter between 0 and 1
G is a directed edge weighted graph
n is the number of vertices
m is the number of edges
"""
def maximizeInfluence(eps, Gt, n, m):
    R = int(144 * n * m * math.log(n) / (float(eps)**3))
    H = buildHyperGraph(R, Gt, n, m)
    return buildSeedSet(H, k)

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
        Z = simulateSpread(Gt, u, H)
        for n in Z:
            H[n].append(Z)
        counter += len(Z)

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
def buildSeedSet(H, k):
    # initialize
    verticesByDegree = [set() for _ in xrange(n)]
    head = -1
    for node, edges in enumerate(H):
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


    

