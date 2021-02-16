import random


def create_cities(n_cities, dimension=2, limits=None, type='int', seed=None):
    """
    :param n_cities: Number of cities in the case
    :param dimension: Dimension of the coordinates
    :param limits: tuple of lists or list of numbers depicting the limits of each dimension.  Must either be an
    interable of length 2, or an iterable of length of dimension in tuples
    :param type: 'int' or 'float'
    :param seed: seed for random number generator
    :return: list of tuple of city locations
    """
    random.seed(seed)
    if not limits:
        LB, UB = 0, pow(n_cities, dimension)
        LB, UB = [LB] * dimension, [UB] * dimension
    elif len(limits) == 2 and all(isinstance(ele, int) or isinstance(ele, int) for ele in limits):
        LB, UB = limits
        LB, UB = [LB] * dimension, [UB] * dimension
    elif len(limits) == dimension and all(isinstance(ele, int) or isinstance(ele, int) for ele in limits):
        LB = [0] * len(limits)
        UB = limits.copy()
    else:
        raise Exception("ERROR IN CITY GENERATION")
    cities = {tuple(random.randint(lb, ub) for lb, ub in zip(LB, UB)) for _ in range(n_cities)}
    while len(cities) < n_cities:
        cities.add(tuple(random.randint(lb, ub) for lb, ub in zip(LB, UB)))
    return list(cities)
