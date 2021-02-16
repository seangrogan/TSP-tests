from distance_metrics import euclidean


def christofides(cities, name=None):
    cities = list(cities)
    dist_matrix = [[euclidean(p1, p2) if i >= j else 0 for i, p1 in enumerate(cities)] for j, p2 in enumerate(cities)]
    csr_dist_matrix = csr_matrix(dist_matrix)
    mst = minimum_spanning_tree(csr_dist_matrix)
    return 0
