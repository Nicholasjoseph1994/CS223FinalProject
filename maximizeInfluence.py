import random
import math
import time
import sys
from collections import Counter
class HashableSet:
    def __init__(self, _set):
        self._set = _set
    def __eq__(self, other):
        return self._set is other._set
    def __hash__(self):
        return id(self._set)


p = .01
eps = .8
k = int(sys.argv[1])

"""
eps is precision parameter between 0 and 1
G is a directed edge weighted graph
n is the number of vertices
m is the number of edges
"""
def maximizeInfluence(eps, Gt, n, m, k):
    R = int(144 * (n + m) * math.log(n) / (float(eps)**3))
    H, degs, twodegs = buildHyperGraph(R, Gt, n, m)
    return buildSeedSet(H, k, R, degs, twodegs)

"""
R is the number of steps to take before terminating
G is a directed edge weighted graph
"""
def buildHyperGraph(R, Gt, n, m):
    #H is a list of lists of sets, h[n][i] is the ith edge that n is in (edges are sets)
    H = [set() for _ in xrange(n)]
    degs = [0 for _ in xrange(n)]
    twodegs = [Counter() for _ in xrange(n)]
    counter = 0
    i = 0
    while counter < R:
        u = random.randrange(n)
        Z = simulateSpread(Gt, [u])
        if len(Z) == 1:
            degs[Z[0]] += 1
        elif len(Z) == 2:
            e1, e2 = Z[0], Z[1]
            twodegs[e1][e2] += 1
            twodegs[e2][e1] += 1
        else:
            for n2 in Z:
                H[n2].add(HashableSet(Z))
        counter += len(Z)
        i += 1
        if i % (R/1000) == 0:
            print 'round %d' % i
    return H, degs, twodegs

"""
Gt is the transpose of the graph
u is the starting node
returns the set of all nodes discovered
"""
def simulateSpread(Gt, vk):
    V = set(vk)
    stack = list(vk)
    while len(stack):
        n = stack.pop()
        for nextVertex in Gt[n]:
            n2 = nextVertex[0]
            if random.random() < nextVertex[1] and n2 not in V:
                stack.append(n2)
                V.add(n2)
    return list(V)

def correctHead (head, setsByDegree):
    while not setsByDegree[head] or len(setsByDegree[head]) == 0:
        head -= 1
    return head

def addToSet(verticesByDegree, degree, node):
    if verticesByDegree[degree]:
        verticesByDegree[degree].add(node)
    else:
        verticesByDegree[degree] = set([node])
"""
H is a hypergraph represented as a set of vertices and a set of sets of vertices
k is the number of seed nodes
"""
def buildSeedSet(H, k, R, degs, twodegs):
    # initialize
    verticesByDegree = [None for _ in xrange(R)]
    head = -1
    for node, edges in enumerate(H):
        addToSet(verticesByDegree, len(edges) + degs[node] + sum(twodegs[node].values()), node)

    print 'building seed set'

    vk = []
    for i in xrange(k):
        head = correctHead(head, verticesByDegree)
        minVertex = verticesByDegree[head].pop()
        vk.append(minVertex)
        counter = 0
        for edge in H[minVertex]:
            for n in edge._set:
                counter += 1
                if n == minVertex:
                    continue
                deg = len(H[n]) + degs[n] + sum(twodegs[n].values())
                H[n].remove(edge)
                verticesByDegree[deg].remove(n)
                addToSet(verticesByDegree, deg-1, n)
        for n, count in twodegs[minVertex].iteritems():
            twodegcount = sum(twodegs[n].values())
            deg = len(H[n]) + degs[n] + twodegcount
            verticesByDegree[deg].remove(n)
            addToSet(verticesByDegree, deg - twodegs[n][minVertex], n)
            del twodegs[n][minVertex]
        H[minVertex] = set()
        print 'found %dth vector' % i

    return vk

def uniformize(G, p):
    for node, edges in enumerate(G):
        G[node] = [(i, p) for i in edges]
    return G

def transpose(G, n):
    G2 = [[] for _ in xrange(n)]

    for n, edges in enumerate(G):
        for (n2, p) in edges:
            G2[n2].append((n, p))

    return G2

def estimateSpread(G, vk):
    counter = 0
    iter = 10000
    for i in xrange(iter):
        n = len(simulateSpread(G, vk))
        counter += n

    return counter / float(iter)

def readGraph(file):
    with open(file, 'r') as f:
        it = iter(f.readlines())
        first = next(it)
        n = int(first.split(' ')[0])
        m = int(first.split(' ')[1])
        G = [[] for _ in xrange(n)]
        for l in it:
            n1, n2 = l.split(' ')[:2]
            G[int(n2)].append(int(n1))
            G[int(n1)].append(int(n2))

    return G, n, m

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


    n = 14
    m = 12

    G = uniformize(G, p)
    G2 = transpose(G, n)

    vk = maximizeInfluence(eps, G2, n, m, k)
    print vk
    print estimateSpread(G, vk)

def test2():
    file = 'hep.txt'
    G, n, m = readGraph(file)
    G = uniformize(G, p)

    vk = maximizeInfluence(eps, G, n, m, k)

    print vk
    print estimateSpread(transpose(G, n), vk)

if __name__ == '__main__':
    #test1()
    test2()
