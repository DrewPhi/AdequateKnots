

def isPositive(crossing):
    return crossing[1] > crossing[3]

def flip_crossing(crossing):
    if isPositive(crossing):
        return [crossing[3], crossing[0], crossing[1], crossing[2]]
    else:
        return [crossing[1], crossing[2], crossing[3], crossing[0]]
def Mirror(pdcode):
    return [flip_crossing(c) for c in pdcode]





def AGraph(pdcode):
    vertex = []
    edge = []

    # Step 1: Process all crossings and build vertex and edge lists
    for i in range(len(pdcode)):
        arc1 = pdcode[i][0]
        arc2 = pdcode[i][1]
        arc3 = pdcode[i][2]
        arc4 = pdcode[i][3]

        # Add edge based on A-resolution
        edge.append([[arc1, arc2], [arc3, arc4]])

        # First pair (arc1, arc2)
        pos1 = [idx for idx, v in enumerate(vertex) if arc1 in v]
        pos2 = [idx for idx, v in enumerate(vertex) if arc2 in v]
        if not pos1 and not pos2:
            vertex.append([arc1, arc2])
        elif pos1 and pos2 and pos1[0] != pos2[0]:
            vertex.append(vertex[pos1[0]] + vertex[pos2[0]])
            for idx in sorted([pos1[0], pos2[0]], reverse=True):
                del vertex[idx]
        elif not pos1 and pos2:
            vertex[pos2[0]].append(arc1)
        elif pos1 and not pos2:
            vertex[pos1[0]].append(arc2)

        # Second pair (arc3, arc4)
        pos3 = [idx for idx, v in enumerate(vertex) if arc3 in v]
        pos4 = [idx for idx, v in enumerate(vertex) if arc4 in v]
        if not pos3 and not pos4:
            vertex.append([arc3, arc4])
        elif pos3 and pos4 and pos3[0] != pos4[0]:
            vertex.append(vertex[pos3[0]] + vertex[pos4[0]])
            for idx in sorted([pos3[0], pos4[0]], reverse=True):
                del vertex[idx]
        elif not pos3 and pos4:
            vertex[pos4[0]].append(arc3)
        elif pos3 and not pos4:
            vertex[pos3[0]].append(arc4)

    # Step 2: Create adjacency matrix
    n = len(vertex)
    adjmatrix = [[0 for _ in range(n)] for _ in range(n)]

    for e in edge:
        e1 = e[0][0]
        e2 = e[1][0]
        edgepos1 = [idx for idx, v in enumerate(vertex) if e1 in v]
        edgepos2 = [idx for idx, v in enumerate(vertex) if e2 in v]
        if edgepos1 and edgepos2:
            i1 = edgepos1[0]
            i2 = edgepos2[0]
            adjmatrix[i1][i2] += 1
            adjmatrix[i2][i1] += 1

    return adjmatrix



def TuraevGenus(pdcode):
    adjmatrixA = AGraph(pdcode)
    adjmatrixB = AGraph(Mirror(pdcode))  # Mirror must be defined elsewhere
    return (len(pdcode) + 2 - len(adjmatrixA) - len(adjmatrixB)) // 2


def AAdequateQ(pdcode):
    adjmatrix = AGraph(pdcode)
    diagonalsum = sum(adjmatrix[i][i] for i in range(len(adjmatrix)))
    return diagonalsum == 0


def BAdequateQ(pdcode):
    return AAdequateQ(Mirror(pdcode))  


def AdequateQ(pdcode):
    return AAdequateQ(pdcode) and BAdequateQ(pdcode)


