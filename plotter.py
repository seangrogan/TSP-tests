from multiprocessing import Process

import matplotlib.pyplot as plt
from grogies_toolbox.auto_mkdir import auto_mkdir
from matplotlib_scalebar.scalebar import ScaleBar

_z_orders = {
    "grid": 0,
    "cities": 300,
    "route": 200
}


def tsp_plotter(title, outfile=None, **kwargs):
    if kwargs.get('mp'):
        Process(target=_tsp_plotter, args=(title, outfile), kwargs=kwargs).start()
    else:
        _tsp_plotter(title, outfile, kwargs)


def _tsp_plotter(title, outfile, kwargs):
    fig, ax = plt.subplots()
    fig.gca().set_aspect("equal", adjustable="box")
    ax.grid(zorder=_z_orders.get("grid", None))
    ax.set_title(label=title)
    if kwargs.get('cities'):
        x, y = zip(*kwargs.get('cities'))
        ax.scatter(x, y, color="green", marker='.', zorder=_z_orders.get("cities", None))
    if kwargs.get('route'):
        route = kwargs.get('route')
        route.append(route[0])
        x, y = zip(*route)
        ax.plot(x, y, color="blue", marker='.', zorder=_z_orders.get("route", None))
    if kwargs.get("scalebar", False):
        _plot_scalebar(ax, fig, **kwargs)
    if outfile:
        auto_mkdir(outfile)
        plt.savefig(outfile)
    if kwargs.get('display', True):
        plt.show()


def _plot_scalebar(ax, fig, **kwargs):
    x1, x2, y1, y2 = ax.axis()
    _y = (y1 + y2) / 2
    scale_bar = ScaleBar(1, location=kwargs.get("location", "lower left"),
                         fixed_value=kwargs.get("fixed_value", None), fixed_units=kwargs.get("fixed_units", None))
    fig.gca().add_artist(scale_bar)
