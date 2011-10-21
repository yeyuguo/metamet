#!/usr/bin/env python
# -*- coding:utf-8 -*-

# filter_cloud.py

#import os, sys
#import re
#from datetime import datetime, timedelta
import numpy as np
#import scipy as sp
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#from matplotlib import mlab
from .lidar import LidarDataset

__all__ = ['filter_cloud']

def filter_cloud(data, gate, repeat=1, start_index=0, fillvalue=np.nan):
    if type(data) is LidarDataset:
        data = data.vars['data']
    gate = np.asarray(gate)
    if gate.shape != tuple() and gate.shape[-1] != 1:
        gate = gate[...,np.newaxis]
    
    cr = data > gate
    cr[..., :start_index] = False
    det = cr[..., repeat-1:].copy()
    for i in range(1,repeat):
        det = det & cr[..., 0+i:-repeat+i]
    final = np.logical_or.accumulate(det, axis=1)
    indexs = (final.argmax(axis=-1) + repeat - 1).reshape(final.shape[0])
#    print indexs
    if start_index < repeat :
        start_index = repeat 
    
    newdata = data.copy()
    for i in range(data.shape[0]):
        if indexs[i] > start_index:
            newdata[i, :, indexs[i]:] = fillvalue
    return newdata

if __name__ == '__main__':
    pass
