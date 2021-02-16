
import pulp
from grogies_toolbox.auto_mkdir import auto_mkdir

from distance_metrics import euclidean
from utilities import problem_name, x_name


def tsp_pulp_dfj(cities, name=None):
    """
    Code for Dantzig–Fulkerson–Johnson formulation of the Travelling salesman problem
    :param cities: list of cities as coordinates
    :param name: name for filenames, etc
    :return: a list of tuples (cities) in the order of travelling
    """
    name = problem_name(name)
    problem = pulp.LpProblem(name, pulp.LpMinimize)
    x = {i: {j: pulp.LpVariable(x_name(i, j), 0, 1, pulp.LpInteger) for j in cities} for i in cities}
    c = {i: {j: euclidean(i, j) for j in cities} for i in cities}
    problem += pulp.lpSum(c[i][j] * x[i][j] for i in cities for j in cities), "ObjFn"
    for j in cities:
        problem += pulp.lpSum(x[i][j] for i in cities if i != j) == 1, f"C1@{j}".replace(' ', '')
        problem += pulp.lpSum(x[j][i] for i in cities if i != j) == 1, f"C2@{j}".replace(' ', '')
        problem += pulp.lpSum(x[j][j]) == 0, f"C3@{j}".replace(' ', '')
    solved = False
    iteration, route = 0, []
    while not solved:
        auto_mkdir(f"./output/lp/dfj-{name}/{name}-dfj-{iteration}.lp")
        problem.writeLP(f"./output/lp/dfj-{name}/{name}-dfj-{iteration}.lp")
        problem.solve()
        route = get_route_from_solution(get_solution_from_x(x), cities)
        route.pop(-1)
        if len(route) == len(cities):
            solved = True
        else:
            subtour_cities = set(route)
            problem += pulp.lpSum(
                x[i][j]
                for i in subtour_cities
                for j in subtour_cities
                if i != j) <= len(subtour_cities) - 1, f"dfj{iteration}"
        iteration += 1
    return route


def get_route_from_solution(sol, cities):
    route = [cities[0], sol[cities[0]]]
    while route[-1] != route[0]:
        route.append(sol[route[-1]])
    return route


def get_solution_from_x(x):
    solution = dict()
    for i, J in x.items():
        for j, var in J.items():
            if var.varValue and var.varValue > 0.9:
                solution[i] = j
    return solution
