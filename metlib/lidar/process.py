#!/usr/bin/env python
# -*- coding:utf-8 -*-

# process.py

import os, sys
#import re
#from datetime import datetime, timedelta
import numpy as np
#import scipy as sp
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#from matplotlib import mlab
from lidar import LidarDataset
__all__ = ['correct_background', 'correct_afterpulse',
        'correct_overlap', 'correct_distance',
        'zero_blind_range']

def correct_background(data, sample_number=None):
    """corrects background noise.
    data: a LidarDataset object
    sample_number: use the last sample_number bins as background.
        if sample_number is None, use lidar data's prvided background.
    """
    if sample_number is None:
        bg = data.vars['background']
    elif sample_number == 0:
        return
    else:
        bg = data.vars['data'][:,:,-sample_number:].mean(axis=-1)
    bg = bg.reshape((bg.shape[0], bg.shape[1], 1))
    data.vars['data'] -= bg
    data.desc += ',background corrected'

def correct_afterpulse(data, ap_data, zero_check_max_index=30):
    """correct afterpulse noise.
    data: a LidarDataset object.
    ap_data: afterpulse data. 
    """
    min_len = np.min((data.dims['BIN'], ap_data.shape[-1]))
    zcmi = np.min((min_len, zero_check_max_index))
    d = data.vars['data']
    d[...,:min_len] -= ap_data[..., :min_len]
    d[...,:zcmi][np.where(d[...,:zcmi] < 0.0)] = 0.0
    
    data.desc += ',afterpulse corrected'

def correct_overlap(data, ol_data):
    """correct overlap.
    data: a LidarDataset object.
    ol_data: overlap data.
    """
    min_len = np.min((data.dims['BIN'], ol_data.shape[-1]))
    data.vars['data'][...,:min_len] *= ol_data[..., :min_len]
    data.desc += ',overlap corrected'

def correct_distance(data):
    """correct distance.
    data: a LidarDataset object.
    """
    data.vars['data'] *= (data.vars['distance'] ** 2 * 1E-6)
    data.desc += ',distance corrected'

def zero_blind_range(data):
    """make the blind range zero.
    data: a LidarDataset object.
    """
    try:
        start_i = data.vars['first_data_bin']
    except:
        start_i = 0
    data.vars['data'][...,:start_i] = 0.0


if __name__ == '__main__':
    pass
