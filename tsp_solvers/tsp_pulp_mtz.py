import pulp
from grogies_toolbox.auto_mkdir import auto_mkdir

from distance_metrics import euclidean
from utilities import problem_name, x_name, u_name


def tsp_pulp_mtz(cities, name=None):
    """
    Code for Miller–Tucker–Zemlin formulation of the Travelling salesman problem
    :param cities: list of cities as coordinates
    :param name: name for filenames, etc
    :return: a list of tuples (cities) in the order of travelling
    """
    name = problem_name(name)
    problem = pulp.LpProblem(name, pulp.LpMinimize)
    x = {i: {j: pulp.LpVariable(x_name(i, j), 0, 1, pulp.LpInteger) for j in cities} for i in cities}
    c = {i: {j: euclidean(i, j) for j in cities} for i in cities}
    problem += pulp.lpSum(c[i][j] * x[i][j] for i in cities for j in cities), "ObjFn"
    u = {i: pulp.LpVariable(u_name(i), 0, None, pulp.LpInteger) for i in cities}
    for j in cities:
        problem += pulp.lpSum(x[i][j] for i in cities if i != j) == 1, f"C1@{j}".replace(' ', '')
        problem += pulp.lpSum(x[j][i] for i in cities if i != j) == 1, f"C2@{j}".replace(' ', '')
    for idx, i in enumerate(cities[1:], 1):
        for j in cities[1:]:
            if i != j:
                problem += u[i] - u[j] + len(cities) * x[i][j] <= len(cities) - 1, f"C3@{i}-{j}".replace(' ', '')
    for i in cities[1:]:
        problem += u[i] <= len(cities) - 1, f"C4a@{i}".replace(' ', '')
        problem += 1 <= u[i], f"C4b@{i}".replace(' ', '')
    problem += u[cities[0]] == 0, f"C5@{cities[0]}(init)"
    auto_mkdir(f"./output/lp/{name}-mtz.lp")
    problem.writeLP(f"./output/lp/{name}-mtz.lp")
    problem.solve()
    solution = [(i, var.varValue) for i, var in u.items()]
    solution.sort(key=lambda ele: ele[1])
    order, *_ = zip(*solution)
    return list(order)
