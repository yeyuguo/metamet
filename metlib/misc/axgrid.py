#!/usr/bin/env python

# misc.py

import os
import re
#from datetime import datetime, timedelta
#from dateutil.parser import parse
import numpy as np
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#from matplotlib import mlab
#from netCDF4 import Dataset

__all__ = ['axgrid']

def axgrid(fig, ncol=2, nrow=2, left=0.1, right=0.1, top=0.1, bottom=0.1, hspace=0.05, vspace=0.05, no_extra_xticklabels=True, no_extra_yticklabels=True, sharex=False, sharey=False, sharexy=False):
    """axgrid creates a grid of axes on a fig.
    Parameters:
        fig: the fig.
        ncol: number of columns.
        nrow: number of rows.
        left: left edge width (0-1).
        right: right edge width (0-1).
        top: top edge width (0-1).
        bottom: bottom edge width (0-1).
        hspace: horizontal space between axes.
        vspace: vertical space between axes.
        no_extra_xticklabels: if True, only xticklabels on the bottom row are presented.
        no_extra_yticklabels: if True, only yticklabels on the left row are presented.
        sharex: if True, axes on each column will share the same xaxis.
        sharey: if True, axes on each row will share the same yaxis.
        sharexy: if True, all axes will share the same xaxis and yaxis.
    Returns:
        an np.ndarray of axes. 
    """
    thegrid = np.zeros((nrow, ncol), dtype='O')

    w = (1.0 - left - right - hspace*(ncol-1)) / ncol
    h = (1.0 - top - bottom - vspace*(nrow-1)) / nrow

    for idx in np.ndindex(nrow, ncol):
        pos = (left+idx[1]*(w+hspace), 1.0-top-h-idx[0]*(h+vspace), w, h)
        sharexyd = dict()
        if sharexy:
            if idx[0] >= 1 or idx[1] >= 1:
                sharexyd['sharex'] = thegrid[0, 0]
                sharexyd['sharey'] = thegrid[0, 0]
        else:
            if sharex and idx[0] >= 1:
                sharexyd['sharex'] = thegrid[0, idx[1]]
            if sharey and idx[1] >= 1:
                sharexyd['sharey'] = thegrid[idx[0], 0]
        thegrid[idx] = fig.add_axes(pos, **sharexyd)

    if no_extra_xticklabels:
        for ax in thegrid[:-1, :].flat:
            plt.setp(ax.get_xticklabels(), visible=False)
    if no_extra_yticklabels:
        for ax in thegrid[:, 1:].flat:
            plt.setp(ax.get_yticklabels(), visible=False)
    return thegrid

