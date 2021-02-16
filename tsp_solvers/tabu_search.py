from collections import namedtuple
from copy import deepcopy
from operator import attrgetter
import random
from time import time
import tqdm
from distance_metrics import euclidean, dist_of_route
from tsp_solvers.tsp_nearest_neighbor import tsp_nearest_neighbor
from plotter import tsp_plotter

tabu_pars = {
    'time_limit': 6000,
    'tabuLen': 100,
    'max_iter': 100_000,
    "iter_no_improve": 1000
}


class TabuStoppingCriteria:
    def __init__(self, time_limit=None, max_iter=None, iter_no_improve=None, *, t_init=time(), **kwargs):
        self.t_start = t_init
        self.time_limit = time_limit
        self.max_iter = max_iter
        self.iter_no_improve = iter_no_improve
        self.max_iter_counter = 0
        self.iter_no_improve_counter = 0
        self.pbar = tqdm.tqdm(desc="TabuSearch")

    def add_stopping_criteria(self, stopping_criteria):
        pass

    def is_done(self, new_best=False, best_value=None):
        self.max_iter_counter += 1
        self.iter_no_improve_counter += 1
        self.pbar.set_postfix_str(f"Current Best Solution {best_value}")
        self.pbar.update()

        if self.time_limit and time() - self.t_start > self.time_limit:
            return True
        if new_best:
            self.iter_no_improve_counter = 0
        if self.max_iter and self.max_iter < self.max_iter_counter:
            return True
        if self.iter_no_improve and self.iter_no_improve < self.iter_no_improve_counter:
            return True
        return False


def slide_cities(solution, neighbors, NewSolution):
    s1, cities = deepcopy(solution), set(solution)
    for city in cities:
        s1.remove(city)
        for i in range(len(s1)):
            s2 = s1[:i] + [city] + s1[i:]
            neighbors.append(NewSolution(s2, city, dist_of_route(s2)))
        s1 = deepcopy(solution)


def shuffle_subset(solution, neighbors, NewSolution):
    s1, cities = deepcopy(solution), set(solution)
    for i in range(len(s1)):
        s2 = s1[:i] + random.sample(s1[i:], len(s1[i:]))
        neighbors.append(NewSolution(s2, f'shuffle{i}', dist_of_route(s2)))


def unknot(solution, neighbors, NewSolution):
    def clean_up_intersections(tour):
        done = False
        cleaned = tour.copy()
        while not done:
            cleaned, done = _clean_up_intersections(cleaned)
        return cleaned

    def ccw(A, B, C):
        Ax, Ay = A[0], A[1]
        Bx, By = B[0], B[1]
        Cx, Cy = C[0], C[1]
        return (Cy - Ay) * (Bx - Ax) > (By - Ay) * (Cx - Ax)
        # Return true if line segments AB and CD intersect

    def intersect(line1, line2):
        A, B = line1[0], line1[1]
        C, D = line2[0], line2[1]
        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

    def _clean_up_intersections(tour):
        clean = tour.copy()
        for p1, p2 in zip(tour, tour[1:]):
            for p3, p4 in zip(tour, tour[1:]):
                if (p1 == p3 and p2 == p4) or (p2 == p3) or (p1 == p4):
                    pass
                else:
                    line1, line2 = (p1, p2), (p3, p4)
                    assert line1 != line2
                    assert p2 != p3 and p1 != p4
                    if intersect(line1, line2):
                        i, j = clean.index(p1), clean.index(p4)
                        clean = clean[:i + 1] + clean[j - 1:i:-1] + clean[j:]
                        return clean, False
        return clean, True

    def test_if_line_intersects(line1, line2):
        p1i, p1j = line1[0], line1[1]
        p2i, p2j = line2[0], line2[1]
        le = max(min(p1i[0], p1j[0]), min(p2i[0], p2j[0]))
        ri = min(max(p1i[0], p1j[0]), max(p2i[0], p2j[0]))
        to = max(min(p1i[1], p1j[1]), min(p2i[1], p2j[1]))
        bo = min(max(p1i[1], p1j[1]), max(p2i[1], p2j[1]))
        if to > bo or le > ri:
            return False
        if (to, le) == (bo, ri):
            return False
        x_1, y_1 = zip(*line1)
        x_2, y_2 = zip(*line2)
        return True

    def line_intersection(line1, line2):
        _x, _y = 0, 1
        d_x = (line1[0][_x] - line1[1][_x], line2[0][_x] - line2[1][_x])
        d_y = (line1[0][_y] - line1[1][_y], line2[0][_y] - line2[1][_y])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        x_1, y_1 = zip(*line1)
        x_2, y_2 = zip(*line2)

        div = det(d_x, d_y)
        if div == 0:
            return False
        d = (det(*line1), det(*line2))
        x = det(d, d_x) / div
        y = det(d, d_y) / div
        return x, y

    s2 = clean_up_intersections(clean_up_intersections(solution))
    neighbors.append(NewSolution(s2, f'unknot@', dist_of_route(s2)))


def get_neighbors(solution):
    neighbors = []
    NewSolution = namedtuple("NewSolution", ['solution', 'move', 'dist'])
    slide_cities(solution, neighbors, NewSolution)
    shuffle_subset(solution, neighbors, NewSolution)
    unknot(solution, neighbors, NewSolution)
    neighbors.sort(key=attrgetter('dist'))
    return neighbors


def tsp_tabu_search(cities, name=None, initial_solution=None):
    if initial_solution is None:
        initial_solution = tsp_nearest_neighbor(cities)
    tabu_stopping_criteria = TabuStoppingCriteria(
        **tabu_pars
    )
    best_solution = deepcopy(initial_solution)
    best_distance = dist_of_route(best_solution, metric=euclidean)
    current_solution = deepcopy(initial_solution)
    current_distance = dist_of_route(current_solution, metric=euclidean)
    tabu_list = []
    new_best = False
    while not tabu_stopping_criteria.is_done(new_best, best_distance):
        new_best = False
        neighbors = get_neighbors(current_solution)
        best_neighbor, move, dist = neighbors.pop(0)
        while move in tabu_list and len(neighbors) > 0:
            best_neighbor, move, dist = neighbors.pop(0)
        if len(neighbors) == 0:
            tabu_list = []
        else:
            current_solution = deepcopy(best_neighbor)
            current_distance = dist_of_route(current_solution, metric=euclidean)
            if current_distance < best_distance:
                best_solution = deepcopy(current_solution)
                best_distance = dist_of_route(best_solution, metric=euclidean)
                new_best = True
            else:
                city = current_solution.pop(0)
                current_solution.append(city)
            tabu_list.append(move)
            if len(tabu_list) > tabu_pars.get('tabuLen', float('inf')):
                tabu_list.pop(0)
    return best_solution
