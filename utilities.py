def problem_name(name):
    return "TSP" if name is None else name


def x_name(i, j):
    name = f"({i}|{j})"
    name.replace(' ', '')
    return name


def u_name(i):
    name = f"({i})"
    name.replace(' ', '')
    return name