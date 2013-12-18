#!/usr/bin/env python2.7

# util.py

import os, sys
import re
#from datetime import datetime, timedelta
#from dateutil.parser import parse
import numpy as np
#import pandas as pd
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import FuncFormatter, FixedFormatter, ScalarFormatter, LogFormatter, FormatStrFormatter
#from mpl_toolkits.basemap import Basemap
#from matplotlib import mlab
#from netCDF4 import Dataset
from metlib import Null, isseq

__all__ = ['format_ticks']

def format_ticks(ax=None, fmt=None, axis='x', fontsize=None, fontweight=None, **kwargs):
    """Format ticks.
    ax: ax, default gca().
    fmt: date format like "%Y%m%d", or format string like "%.2f", or a func, or sequence of strs, or sequence of (position, str), default None.
    axis: 'x' | 'y' | 'z', default 'x'.
    fontsize: fontsize, default None.
    fontweight: fontweight, default None.
    """
    if not ax:
        ax = plt.gca()

    if axis == 'x':
        theaxis = ax.xaxis
    elif axis == 'y':
        theaxis = ax.yaxis
    elif theaxis == 'z':
        theaxis = ax.zaxis
    else:
        theaxis = Null

    if fmt:
        datefmt_pattern = r'%H|%I|%M|%S|%Y|%y|%m|%w|%W|%a|%A|%b|%B|%p|%z|%Z|%j|%U|%c|%x|%X'
        str_pattern = r'%'
        if callable(fmt):
            fmt = FuncFormatter(fmt)
        elif isinstance(fmt, (str, unicode, np.string_)):
            if re.search(datefmt_pattern, fmt):
                fmter = DateFormatter(fmt)
            elif re.search(str_pattern, fmt):
                fmter = FormatStrFormatter(fmt)
            else:
                fmter = Null
        elif isseq(fmt):
            if np.ndim(fmt) == 1:
                fmter = FixedFormatter(fmt)
            elif np.ndim(fmt) == 2 and np.shape(fmt)[1] == 2:
                fmt = np.array(fmt)
                pos = fmt[:, 0]
                fmter = FixedFormatter(fmt[:,1])
                theaxis.set_ticks(pos)
            else:
                fmter = Null
        else:
            fmt = Null

        if fmter:
            theaxis.set_major_formatter(fmter)

    if fontsize:
        plt.setp(theaxis.get_ticklabels(), fontsize=fontsize)

    if fontweight:
        plt.setp(theaxis.get_ticklabels(), fontweight=fontweight)

if __name__ == '__main__':
    pass
