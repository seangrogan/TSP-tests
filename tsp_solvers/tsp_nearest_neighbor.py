import random

from distance_metrics import euclidean
from utilities import problem_name


def tsp_nearest_neighbor(cities, name=None):
    """
    Nearest Neighbor Algorithm
    :param cities:
    :param name:
    :return:
    """
    name = problem_name(name)
    city = random.choice(cities)
    c = {i: {j: euclidean(i, j) for j in cities if i != j} for i in cities}
    route = [city, ]
    while len(route) < len(cities):
        next_cities = c[route[-1]]
        key = max(next_cities, key=next_cities.get)
        if key in route:
            c[route[-1]].pop(key)
        else:
            route.append(key)
    return route
