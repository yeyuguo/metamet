#!/usr/bin/env python

# lidarutil.py

import os, sys
#import re
#from datetime import datetime, timedelta
import numpy as np
#import scipy as sp
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#from matplotlib import mlab
from .constant import lidar_sm

def height_to_index(height, data, elev_angle, use_float_index=False, offset=None):
    """height: in m.
    offset: lidar offset of distance, usually positive.
    """
    start_i = data['first_data_bin']
    bin_size = data['bin_size']
    dist = np.array(height) / np.sin(np.deg2rad(elev_angle))
    if offset is None:
        float_index = dist / bin_size - 0.5 + start_i
    else:
        float_index = (dist + offset) / bin_size 
    if use_float_index:
        return float_index
    else:
        float_index[np.where(~np.isfinite(float_index))] = -1.0
        return np.round(float_index).astype('i')

if __name__ == '__main__':
    pass
