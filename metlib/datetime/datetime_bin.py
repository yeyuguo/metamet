#!/usr/bin/env python
# -*- coding:utf-8 -*-

# datetime_bin.py
"""This module provides functions on binning and averaging data"""

import os, sys
#import re
from datetime import datetime, timedelta
import numpy as np
#import scipy as sp
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#from matplotlib import mlab
__all__ = ['datetime_bin'] 
def datetime_bin(datetimes, tdelta, starttime=None, endtime=None, return_bin_info=False):
    """This function parti...TODO a serie of datetime objects into equal timedelta bin. 
    Returns a list of np.where style tuples. If return_bin_info is True, also returns a list of (bin_start, bin_end) tuples.
    Parameters:
    datetimes is a seq of datetime objects, 
    tdelta is a timedelta object,
    starttime is a datetime object or None. When it's None, use the first datetime in the input sequence as starttime
    endtime is a datetime object or None. When it's None, use the last datetime in the input sequence as endtime
    """
    if starttime is None:
        starttime = datetimes[0]
    if endtime is None:
        endtime = datetimes[-1] + tdelta / 2
    tmpbin_start = starttime
    result = []
    bin_info = []
    tmpbin = []
    tmpbin_end = tmpbin_start + tdelta
    i = 0
    while tmpbin_start < endtime:
        if i == len(datetimes) or datetimes[i] >= tmpbin_end:
            bin_info.append((tmpbin_start, tmpbin_end))
            result.append((np.array(tmpbin, dtype='i8'), ))
            tmpbin = []
            tmpbin_start, tmpbin_end = tmpbin_end, tmpbin_end + tdelta
        elif datetimes[i] < tmpbin_start:
            i += 1
        else:
            tmpbin.append(i)
            i += 1
            
    if return_bin_info is True:
        return result, bin_info
    else:
        return result


if __name__ == '__main__':
    pass
