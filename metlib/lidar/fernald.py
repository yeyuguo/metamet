#!/usr/bin/env python
# -*- coding:utf-8 -*-

# fernald.py

import os, sys
#import re
#from datetime import datetime, timedelta
import numpy as np
#import scipy as sp
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#from matplotlib import mlab
from metlib.lidar.constant import lidar_sm

__all__ = ['fernald']
def fernald(data, lidar_constant, lidar_ratio, intbm, C_contains_E=False):
    """fernald 1984's retrieval method.
    data: a LidarDataset object which contains normalized data.
    lidar_constant: lidar constant.
    lidar_ratio: lidar ratio.
    intbm: \int^{0}_{r}betam(z)*dz.
    """
    dz = data.vars['bin_size']
    try:
        start_i = data.vars['first_data_bin']
    except:
        start_i = 0
    CE = np.zeros_like(data.vars['data'])
    if C_contains_E:
        CE[:] = lidar_constant
    else:
        CE[:] = lidar_constant * data.vars['energy'].reshape((CE.shape[0],CE.shape[1],1))
#    print "CE: ", CE.shape
    plt.figure()
    plt.pcolormesh(CE[:,0,:])
    plt.colorbar()
    plt.title("CE")

    expIntBm = np.exp(-2.0*(lidar_ratio-lidar_sm)*intbm)
#    print "expIntBm: ", expIntBm.shape
    plt.figure()
    plt.plot(expIntBm)
    plt.title("expIntBm")

    XexpIntBm = data.vars['data'] * expIntBm
#    print "XexpIntBm: " , XexpIntBm.shape
    plt.figure()
    plt.pcolormesh(XexpIntBm[:,0,:])
    plt.colorbar()
    plt.title("XexpIntBm")

    intXexpIntBm = np.zeros_like(XexpIntBm)
    intXexpIntBm[...,start_i:] = np.add.accumulate(XexpIntBm[...,start_i:] * dz, axis=-1)
#    print "intXexpIntBm: " , intXexpIntBm.shape
    plt.figure()
    plt.pcolormesh(intXexpIntBm[:,0,:])
    plt.colorbar()
    plt.title("intXexpIntBm")

    bottom_term = CE - 2.0 * lidar_ratio * intXexpIntBm
#    print "bottom_term:" , bottom_term.shape
    plt.figure()
    plt.pcolormesh(bottom_term[:,0,:])
    plt.colorbar()
    plt.title("bottom")

    ba = XexpIntBm / bottom_term
    ba[...,start_i:] = 0.0
#    print "ba: ", ba.shape
    plt.figure()
    plt.pcolormesh(ba[:,0,:])
    plt.colorbar()
    plt.title("ba")

    data.vars['data'] = ba
    data.desc += ',retrievaled'


if __name__ == '__main__':
    pass
