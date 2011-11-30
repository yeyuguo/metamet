import numpy as np
import matplotlib
import matplotlib.pyplot as plt
__all__ = ['plot_lidar']

def plot_lidar(dts, height, data, 
        vmin=None, vmax=None, max_height=5000,
        title='', xlabel=None, ylabel='Height (m)', 
        cmap=matplotlib.cm.jet,
        figsize=(12,6)
        ):
    """Plot lidar image and returns a fig.
    dts: datetime seq
    height: height seq
    data: data of shape ( TIME, HEIGHT )
    vmin, vmax: value range
    max_height: plot max height.
    title: plot title
    xlabel, ylabel: Labels
    cmap: colormap
    figsize: figsize
    """
    if vmin is None:
        vmin = 0.0
    if vmax is None:
        vmax = data.max()
    if xlabel is None:
        xlabel = '%s - %s' % (dts[0], dts[-1])
    dts_num = matplotlib.dates.date2num(dts)
    fig = plt.figure(figsize=figsize)
    ax = plt.pcolormesh(dts_num, height, np.ma.masked_invalid(data.transpose()), vmin=vmin, vmax=vmax)
    plt.gca().get_xaxis().axis_date()
    plt.gca().tick_params(direction='out', labelsize='x-small')
    fig.autofmt_xdate()
    plt.ylim(0.0, max_height)
    cbar = plt.colorbar(fraction=0.05)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    return fig
