# An effective approach to controller placement in software defined wide area networks
import numpy as np

def init_dict(key):
    C = {}
    for i in range(len(key)):
        C[key[i]] = []
    return C


def distribute_vertex(centroid, C, latency):
    m, n = latency.shape
    for i in range(n):
        temp = latency[:,i]
        temp = temp[centroid]  # latency from switch i to all centroid
        temp = temp.tolist()
        clind = temp.index(min(temp))
        C[centroid[clind]].append(i)
    return C


def update_centroid(centroid, C, latency):
    newC = {}
    newCentroid = []
    for cent in range(len(centroid)):  # iterate all clusters
        vertex = C[centroid[cent]]  # get the vertexes belongs to cluster "centroid[cent]"
        sumLaten = []
        for v in range(len(vertex)):  # iterate all vertexes inside cluster "centroid[cent]"
            temp = latency[vertex[v]]
            temp = temp[vertex]
            sumLaten.append(sum(temp))
        c = sumLaten.index(min(sumLaten))
        newC[vertex[c]] = vertex
        newCentroid.append(vertex[c])
    return newCentroid, newC


def add_newCentroid(centroid, latency):
    m, n = latency.shape
    potentialCen = np.ones(m)  # potential centroid locations indicated with value 1
    np.put(potentialCen,centroid,[0]*len(centroid))
    noncentroid = np.nonzero(potentialCen)[0]  # index of potential centroids
    sumLaten = []
    for i in range(len(noncentroid)):
        temp = latency[noncentroid[i]]
        temp = temp[centroid]
        sumLaten.append(sum(temp))
    ind = sumLaten.index(max(sumLaten))
    newCentroid = noncentroid[ind]
    return newCentroid


def network_partition(D, clusterNum):
    # input: D is a 2D numpy array describing the distance among any two points,
    # k is the number of clusters
    # tmax is the maximum iteration time
    # output: the centroids of k clusters
    # mapping from switches to clusters

    m, n = D.shape  # m: potential controller locations, n: switch locations

    if clusterNum > m:
        raise Exception('too many centroids')

    centroid = []
    C = {}

    sumLaten = []
    for i in range(m):
        sumLaten.append(sum(D[i]))

    # the node with smallest sum end-to-end latency to other nodes is selected as the centroid
    c1 = sumLaten.index(min(sumLaten))
    centroid.append(c1)
    if clusterNum == 1:
        C[c1] = range(m)
        return centroid, C

    # add the other clusterNum-1 centroids
    for k in range(clusterNum-1):
        # find the node with biggest end-to-end latency to the centroid as the second centroid
        # temp = D[c1].tolist()
        # c2 = temp.index(max(temp))
        c2 = add_newCentroid(centroid, D)
        centroid.append(c2)
        C = init_dict(centroid)   # initialize a dictionary to represent clusters
        C = distribute_vertex(centroid, C, D)
        centroid,C = update_centroid(centroid, C, D)

    return centroid, C

