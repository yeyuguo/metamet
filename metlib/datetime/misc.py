#!/usr/bin/env python
# -*- coding:utf-8 -*-

# misc.py

#import os, sys
#import re
from datetime import datetime, timedelta
import numpy as np
#import scipy as sp
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#from matplotlib import mlab
__all__ = ['month2season', 'str2datetime']

def month2season(month, outformat='0123'):
    """Converts month number ( 1-12 ) to season number or names.
    Parameters:
        month : int or seq of int ( 1 - 12 )
        outformat: '0123', '1234', 'name' or ANY seq with at least 4 elements
"""
    if outformat == 'name':
        season_names = np.array(['Spring', 'Summer', 'Autumn', 'Winter'], dtype='O')
    elif outformat == '0123':
        season_names = np.array([0,1,2,3], dtype='i4')
    elif outformat == '1234':
        season_names = np.array([1,2,3,4], dtype='i4')
    else:
        if len(outformat) < 4:
            raise ValueError, 'outformat: "%s" length less than 4' % outformat
        season_names = np.array(list(outformat))

    season_index = (np.array(month, dtype=int)+9) / 3 % 4
    return season_names[season_index]

def str2datetime(fmt='%Y-%m-%d %H:%M:%S', *arrays ):
    """Converts str arrays into datetime arrays.
    Parameters:
        fmt: datetime format string. When using more than one array as input, extra white space should be added. 
        arrays: string or int arrays to parse.
    Returns:
        datetime array
    """
    # TODO: int array not working well now. add something to format int arrays into str first.
    n = len(arrays)
    l = len(arrays[0])
    res = np.zeros(l, dtype='O')
    for i in range(l):
        try:
            datestrs = []
            for j in range(n):
                datestrs.append(str(arrays[j][i]))
            datestr = ' '.join(datestrs)
            res[i] = datetime.strptime(datestr, fmt)
        except Exception, e:
            print e
            res[i] = None
    return res

