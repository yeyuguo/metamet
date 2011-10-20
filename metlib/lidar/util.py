#!/usr/bin/env python
# -*- coding:utf-8 -*-

# util.py

import os, sys
#import re
#from datetime import datetime, timedelta
import numpy as np
#import scipy as sp
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#from matplotlib import mlab
from .constant import lidar_sm

def height_to_index(height, data, elev_angle, use_float_index=False):
    """height: in m.
    """
    start_i = data.vars['first_data_bin']
    bin_size = data.vars['bin_size']
    dist = np.array(height) / np.sin(np.deg2rad(elev_angle))
    float_index = dist / bin_size - 0.5 + start_i
    if use_float_index:
        return float_index
    else:
        return np.round(float_index).astype('i')

if __name__ == '__main__':
    pass
