#!/usr/bin/env python

# alias.py

#import re
#from datetime import datetime, timedelta
#from dateutil.parser import parse
import numpy as np
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#from matplotlib import mlab
#from netCDF4 import Dataset

__all__ = ['ma_out']

def ma_out(arr, vmin=-np.inf, vmax=np.inf):
    """masked values outside (vmin, vmax) and invalid values.
    """
    return np.ma.masked_outside(np.ma.masked_invalid(arr), vmin, vmax)

if __name__ == '__main__':
    pass
