import numpy as np
from functools import lru_cache

class DisjointSet:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        self.parent[self.find(x)] = self.find(y)

def isPositive(crossing):
    return crossing[1] > crossing[3]

def flip_crossing(crossing):
    if isPositive(crossing):
        return [crossing[3], crossing[0], crossing[1], crossing[2]]
    else:
        return [crossing[1], crossing[2], crossing[3], crossing[0]]

@lru_cache(maxsize=512)
def Mirror_cached(pdcode_tuple):
    pdcode = [list(c) for c in pdcode_tuple]
    return tuple(tuple(flip_crossing(c)) for c in pdcode)

def Mirror(pdcode):
    return [list(c) for c in Mirror_cached(tuple(tuple(c) for c in pdcode))]

def AGraph(pdcode):
    dsu = DisjointSet()
    edge_pairs = []

    for a, b, c, d in pdcode:
        dsu.union(a, b)
        dsu.union(c, d)
        edge_pairs.append((a, c))

    comp_map = {}
    index = 0
    for arc in dsu.parent:
        rep = dsu.find(arc)
        if rep not in comp_map:
            comp_map[rep] = index
            index += 1

    size = len(comp_map)
    adj = np.zeros((size, size), dtype=int)
    for a, c in edge_pairs:
        i = comp_map[dsu.find(a)]
        j = comp_map[dsu.find(c)]
        adj[i, j] += 1
        adj[j, i] += 1

    return adj

def AAdequateQ(pdcode, adjmatrix=None):
    if adjmatrix is None:
        adjmatrix = AGraph(pdcode)
    return np.all(np.diag(adjmatrix) == 0)

def BAdequateQ(pdcode):
    mirror_pdcode = Mirror(pdcode)
    return AAdequateQ(mirror_pdcode)

def AdequateQ(pdcode):
    mirror_pdcode = Mirror(pdcode)
    adjA = AGraph(pdcode)
    adjB = AGraph(mirror_pdcode)
    return AAdequateQ(pdcode, adjA) and AAdequateQ(mirror_pdcode, adjB)

def TuraevGenus(pdcode):
    mirror_pdcode = Mirror(pdcode)
    adjA = AGraph(pdcode)
    adjB = AGraph(mirror_pdcode)
    return (len(pdcode) + 2 - len(adjA) - len(adjB)) // 2
