def euclidean(p1, p2):
    return pow(sum(pow(i - j, 2) for i, j in zip(p1, p2)), 0.5)


def dist_of_route(route, metric=None):
    if not metric:
        metric = euclidean
    _route = route + [route[0]]
    dist = sum(metric(i, j) for i, j in zip(_route, _route[1:]))
    return dist
