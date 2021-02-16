from plotter import tsp_plotter
from tsp_case_creator import create_cities
from tsp_solvers.christofides import christofides
from tsp_solvers.tabu_search import tsp_tabu_search
from tsp_solvers.tsp_nearest_neighbor import tsp_nearest_neighbor
from tsp_solvers.tsp_pulp_dfj import tsp_pulp_dfj
from tsp_solvers.tsp_pulp_mtz import tsp_pulp_mtz
from distance_metrics import euclidean, dist_of_route
from timeit import default_timer as timer


def main(n_cities=10, name=None, router=None):
    name = "TSP" if name is None else name
    cities = create_cities(n_cities)
    tsp_plotter(f"{name}", f"./output/img/{name}.png", cities=cities)
    if not isinstance(router, list):
        route = router(cities, name)
        start = timer()
        tsp_plotter(f"{name}-Solution-{router.__name__}-{timer() - start:.3f}s",
                    f"./output/img/{name}-Solution-{router.__name__}-{timer() - start:.3f}s.png",
                    cities=cities,
                    route=route)
    for route_maker in router:
        start = timer()
        route = route_maker(cities, name)
        dist = dist_of_route(route, metric=euclidean)
        new_name = f"{name}-Solution-{route_maker.__name__}-{dist:.3f}d-{timer() - start:.3f}s"
        tsp_plotter(new_name,
                    f"./output/img/{new_name}.png",
                    cities=cities,
                    route=route)


if __name__ == '__main__':
    router = [
        tsp_tabu_search,
        # christofides,
        # tsp_nearest_neighbor,
        # tsp_pulp_mtz,
        tsp_pulp_dfj
    ]

    for i in range(31, 51):
        main(i, name=f"TSP-{i:03d}", router=router)
