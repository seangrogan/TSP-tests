from distance_metrics import euclidean
from utilities import problem_name


def tsp_bhk_algorithm(cities, name=None):
    """
    Bellman–Held–Karp algorithm
    :param cities:
    :param name:
    :return:
    """
    name = problem_name(name)
    c = {i: {j: euclidean(i, j) for j in cities} for i in cities}
    return 0