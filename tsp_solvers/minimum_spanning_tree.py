from math import log10, log


def minimum_spanning_tree(points):
    # m is number of edges, n is number of vertices
    n = len(points)
    m = n * (n-1)/2
    r = log(log(log(n)))
    return mst