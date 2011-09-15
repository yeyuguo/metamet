#!/usr/bin/env python
# -*- coding:utf-8 -*-

# fernald.py

import os, sys
#import re
#from datetime import datetime, timedelta
import numpy as np
from numpy import ma
#import scipy as sp
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#from matplotlib import mlab
from metlib.lidar.constant import lidar_sm

__all__ = ['fernald']
def fernald(data, lidar_constant, lidar_ratio, betam, C_contains_E=False, apply_on_data=False):
    """fernald 1984's retrieval method.
    data: a LidarDataset object which contains normalized data.
    lidar_constant: lidar constant.
    lidar_ratio: lidar ratio.
    intbm: \int^{0}_{r}betam(z)*dz.a
    C_contains_E: whether the lidar constant is C or C*E
    apply_on_data: whether to apply the result on data.
    """
    try:
        start_i = data.vars['first_data_bin']
    except:
        start_i = 0
    dz = data.vars['bin_size'] / 1000.0    # convert to km
    intbm = np.zeros_like(betam)
    intbm[..., start_i:] = np.add.accumulate(betam[..., start_i:]*dz)
    CE = np.zeros_like(data.vars['data'])
    if C_contains_E:
        CE[:] = lidar_constant
    else:
        CE[:] = lidar_constant * data.vars['energy'].reshape((CE.shape[0],CE.shape[1],1))
#    print CE
#    print "CE: ", CE.shape
#    plt.figure()
#    plt.pcolormesh(ma.masked_invalid(CE[:,0,:]))
#    plt.colorbar()
#    plt.title("CE")
#
#    plt.figure()
#    plt.pcolormesh(data.vars['data'][:,0,:], vmin=0.0, vmax=0.1)
#    plt.colorbar()
#    plt.title("X")

    expIntBm = np.exp(-2.0*(lidar_ratio-lidar_sm)*intbm)
#    print "expIntBm: ", expIntBm.shape
#   plt.figure()
#   plt.plot(expIntBm)
#   plt.title("expIntBm")

    XexpIntBm = data.vars['data'] * expIntBm
#    print "XexpIntBm: " , XexpIntBm.shape
#    plt.figure()
#    plt.pcolormesh(ma.masked_invalid(XexpIntBm[:,0,:]), vmin=0, vmax=0.20)
#    plt.colorbar()
#    plt.title("XexpIntBm")

    intXexpIntBm = np.zeros_like(XexpIntBm)
    intXexpIntBm[...,start_i:] = np.add.accumulate(XexpIntBm[...,start_i:] * dz, axis=-1)
#    print "intXexpIntBm: " , intXexpIntBm.shape
#    plt.figure()
#    plt.pcolormesh(ma.masked_invalid(intXexpIntBm[:,0,:]), vmin=0.0, vmax=0.4)
#    plt.colorbar()
#    plt.title("intXexpIntBm")

    bottom_term = CE - 2.0 * lidar_ratio * intXexpIntBm
#    print "bottom_term:" , bottom_term.shape
#   plt.figure()
#   plt.pcolormesh(ma.masked_invalid(bottom_term[:,0,:]))
#   plt.colorbar()
#   plt.title("bottom")

    ba = XexpIntBm / bottom_term - betam 
    ba[...,:start_i] = 0.0
    sigma_a = ba * lidar_ratio
#    print "ba: ", ba.shape
#   plt.figure()
#   plt.pcolormesh(ma.masked_invalid(ba[:,0,:]), vmin=0.0, vmax=0.0005)
#   plt.colorbar()
#   plt.title("ba")

    if apply_on_data:
        data.vars['data'] = sigma_a
        data.desc += ',retrievaled'
    
    return sigma_a.copy()


if __name__ == '__main__':
    pass
