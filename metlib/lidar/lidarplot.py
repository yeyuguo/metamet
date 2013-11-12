import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from metlib import T, TD
__all__ = ['plot_lidar_on_ax', 'plot_lidar', 'LidarPlot']

def plot_lidar_on_ax(dts, height, data, 
        ax, cax=None,
        vmin=None, vmax=None, max_height=5000,
        title='', xlabel=None, ylabel='Height (m)', 
        cmap=matplotlib.cm.jet, colorbar_extend='neither',
        **kwargs
        ):
    """Plot lidar image on a given ax.
    dts: datetime seq
    height: height seq
    data: data of shape ( TIME, HEIGHT )
    ax: the ax on which it is plotted
    cax: ax to plot colorbar. if cax == None, use ax's space.
    vmin, vmax: value range
    max_height: plot max height.
    title: plot title
    xlabel, ylabel: Labels
    cmap: colormap
    figsize: figsize
    kwargs: will be passed to pcolormesh

    returns the pcolormesh image
    """
    if vmin is None:
        vmin = 0.0
    if vmax is None:
        vmax = data.max()
    if xlabel is None:
        xlabel = '%s - %s' % (dts[0], dts[-1])
    
    tdelta = dts[-1] - dts[0]
    if tdelta > TD('24h'):
        dtfmt = DateFormatter('%H\n%m/%d')
    elif tdelta >= TD('6h'):
        dtfmt = DateFormatter('%H')
    elif tdelta >= TD('5m'):
        dtfmt = DateFormatter('%H:%M')
    else:
        dtfmt = DateFormatter('%H:%M:%S')
    dts_num = matplotlib.dates.date2num(dts)
    image = ax.pcolormesh(dts_num, height, np.ma.masked_invalid(data.transpose()), vmin=vmin, vmax=vmax, cmap=cmap, **kwargs)
    ax.xaxis.axis_date()
    ax.xaxis.set_major_formatter(dtfmt)
    plt.setp(ax.xaxis.get_ticklabels(), fontsize='x-small')
    plt.setp(ax.yaxis.get_ticklabels(), fontsize='small')
    ax.set_ylim(0.0, max_height)
    if cax is None or cax == ax:
        cbar = plt.colorbar(image, ax=ax, fraction=0.05, extend=colorbar_extend)
    else:
        cbar = plt.colorbar(image, cax=cax, extend=colorbar_extend)
    ax.set_title(title)
    ax.set_xlabel(xlabel, fontsize='small')
    ax.set_ylabel(ylabel)
    return image

def plot_lidar(dts, height, data, 
        vmin=None, vmax=None, max_height=5000,
        title='', xlabel=None, ylabel='Height (m)', 
        cmap=matplotlib.cm.jet, colorbar_extend='neither',
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
    ax = plt.pcolormesh(dts_num, height, np.ma.masked_invalid(data.transpose()), vmin=vmin, vmax=vmax, cmap=cmap)
    plt.gca().get_xaxis().axis_date()
    plt.gca().tick_params(direction='out', labelsize='x-small')
    fig.autofmt_xdate()
    plt.ylim(0.0, max_height)
    cbar = plt.colorbar(fraction=0.05, extend=colorbar_extend)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    return fig

class LidarPlot(object):
    def __init__(self, dts, height, data,
            vmin=None, vmax=None, max_height=5000,
            title='', xlabel=None, ylabel='Height (m)',
            cmap=matplotlib.cm.jet, colorbar_extend='neither',
            fig=None, figsize=(12,6)):
        """dts: datetime seq
        height: height seq
        data: data of shape ( TIME, HEIGHT )
        vmin, vmax: value range
        max_height: plot max height.
        title: plot title
        xlabel, ylabel: Labels
        cmap: colormap
        figsize: figsize
        """
        self._inited = False
        # Fig and Axes:
        if fig is None:
            self.fig = plt.figure(figsize=figsize)
            self._remember_to_clf = True
        else:
            self.fig = fig
            self._remember_to_clf = False
        self.ax = self.fig.add_axes((0.07, 0.10, 0.73, 0.7))
        self.cax = self.fig.add_axes((0.92, 0.10, 0.03, 0.7))
        self.hax = self.fig.add_axes((0.07, 0.80, 0.73, 0.10))#, sharex=self.ax)
        self.vax = self.fig.add_axes((0.80, 0.10, 0.10, 0.7), sharey=self.ax)
        self.sax = self.fig.add_axes((0.80, 0.80, 0.10, 0.10))
        plt.setp(self.hax.get_xticklabels(), visible=False)
        plt.setp(self.vax.get_yticklabels(), visible=False)
        for ax in (self.ax, self.cax, self.hax, self.vax, self.sax):
            plt.setp(ax.get_xticklabels(), fontsize=9)
            plt.setp(ax.get_yticklabels(), fontsize=9)

        self.update_data(dts, height, data, max_height, vmin, vmax, cmap)
        self._inited = True
        self.suptitle = self.fig.suptitle(title)
        self.xlabel = self.ax.set_xlabel(xlabel)
        self.ylabel = self.ax.set_ylabel(ylabel)
        self.update()
    
    def update_data(self, dts, height, data, max_height=None, vmin=None, vmax=None, cmap=None):
        # Data:
        self.dtsnum = matplotlib.dates.date2num(dts)
        self.height = height
        if self._inited:
            # todo
            vmin, vmax = self.image.get_clim()
            cmap = self.image.get_cmap()
            ylims = self.ax.get_ylim()
            self.cax.cla()
            del self.colorbar
            self.ax.cla()
            del self.image
            self.image = self.ax.pcolormesh(self.dtsnum, self.height, np.ma.masked_invalid(data.transpose()), vmin=vmin, vmax=vmax, cmap=cmap)
            self.ax.set_ylim(ylims)
            self.colorbar = plt.colorbar(self.image,cax=self.cax, extend=colorbar_extend)
        else:
            self.image = self.ax.pcolormesh(self.dtsnum, self.height, np.ma.masked_invalid(data.transpose()), vmin=vmin, vmax=vmax, cmap=cmap)
            self.colorbar = plt.colorbar(self.image,cax=self.cax, extend=colorbar_extend)
            self.ax.set_ylim(0, max_height)
        self.ax.get_xaxis().axis_date()
        self.hax.get_xaxis().axis_date()
        self.fig.autofmt_xdate()
#        print "reseting fontsize"
        for ax in (self.ax, self.cax, self.hax, self.vax, self.sax):
            plt.setp(ax.get_xticklabels(), fontsize=9)
            plt.setp(ax.get_yticklabels(), fontsize=9)
        
    def update(self):
        self.hax.set_xlim(self.ax.get_xlim())
        plt.draw()
#        self.fig.draw_artist(self.hax)

    def xy2ij(self, x, y):
        ix = np.argmin(np.abs(x - self.dtsnum))
        jy = np.argmin(np.abs(y - self.height))
        return ix, jy

    def __del__(self):
        try:
            if self._remember_to_clf == True:
                self.fig.clf()
        except Exception as e:
            print e

 
if __name__ == '__main__':
    p = LidarPlot(None)
    plt.show()
