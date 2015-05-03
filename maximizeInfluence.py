"""
eps is precision parameter between 0 and 1
G is a directed edge weighted graph
n is the number of vertices
m is the number of edges
"""
def maximizeInfluence(eps, G, n, m):
    R = int(144 * n * m * Math.log(n) / (float(eps)**3))
    H = buildHypergraph(R, G, n, m)
    return buildSeedSet(H, k)

"""
R is the number of steps to take before terminating
G is a directed edge weighted graph
"""
def buildHyperGraph(R, G, n, m):
    H = (set(range(n)), set())
    counter = 0
    Gt = transpose(g)
    while counter < R:
        u = random.randrange(n)
        Z = simulateSpread(Gt, u)
        H[1].add(Z)
        counter += len(Z)

"""
Gt is the transpose of the graph
u is the starting node
returns the set of all nodes discovered
"""
def simulateSpread(Gt, u):
    stack = [u]
    while len(stack):
        n = stack.pop(0)
        for nextVertex in Gt[u]:
            

"""
H is a hypergraph represented as a set of vertices and a set of sets of vertices
k is the number of seed nodes
"""
def buildSeedSet(H, k):
    pass
