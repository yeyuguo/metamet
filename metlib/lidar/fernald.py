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
from .constant import lidar_sm
from .util import height_to_index
from .process import fill_lower_part

__all__ = ['fernald', 'fernald_ref']
def fernald(data, lidar_constant, lidar_ratio, betam, fill_index=0, fill_aver_num=1, C_contains_E=False, apply_on_data=False):
    """fernald 1984's retrieval method.
    data: a LidarDataset object which contains normalized data.
    lidar_constant: lidar constant.
    lidar_ratio: lidar ratio.
    betam: molecular backscatter
    fill_index: data below this index will be filled with value above
    fill_aver_num: fill lower part with this number of samples
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
    fill_lower_part(sigma_a, fill_index, fill_aver_num)
#    print "ba: ", ba.shape
#   plt.figure()
#   plt.pcolormesh(ma.masked_invalid(ba[:,0,:]), vmin=0.0, vmax=0.0005)
#   plt.colorbar()
#   plt.title("ba")

    if apply_on_data:
        data.vars['data'] = sigma_a
        data.desc += ',retrievaled'
    
    return sigma_a.copy()


def fernald_ref(data, lidar_ratio, betam, ref_height, ref_sigma_a, ref_aver_num, elev_angle=90.0, apply_on_data=False):
    # TODO: implement fernald_backward
    """fernald 1984's retrieval method.
    data: a LidarDataset object which contains normalized data.
    lidar_ratio: lidar ratio.
    betam: molecular backscater
    ref_height: reference height (m)
    ref_sigma_a: reference aerosol extinction ( km^{-1} )
    ref_aver_num: average several points around that height.
    elev_angle: elev angle of lidar.
    apply_on_data: whether to apply the result on data.
    """
    try:
        start_i = data.vars['first_data_bin']
    except:
        start_i = 0
    dz = data.vars['bin_size'] / 1000.0    # convert to km

    ref_index = height_to_index(ref_height, data, elev_angle)[0]
    ref_beg_index = ref_index - ref_aver_num / 2
    ref_end_index = ref_beg_index + ref_aver_num
    Xref = np.ma.masked_invalid(data.vars['data'][..., ref_beg_index:ref_end_index]).mean(axis=-1)[..., np.newaxis]
    Xref_beta = Xref / (betam[ref_index] + ref_sigma_a / sa)

    intbm = np.zeros_like(betam)
    intbm[..., ref_index:] = np.add.accumulate(betam[..., ref_index:]*dz, axis=-1)
    intbm[..., ref_index-1::-1] = np.add.accumulate(-betam[...,ref_index-1::-1]*dz, axis=-1)

    expIntBm = np.exp(-2.0*(lidar_ratio-lidar_sm)*intbm)

    XexpIntBm = data.vars['data'] * expIntBm

    intXexpIntBm = np.zeros_like(XexpIntBm)
    intXexpIntBm[...,ref_index:] = np.add.accumulate(XexpIntBm[..., ref_index:]*dz, axis=-1)
    intXexpIntBm[...,ref_index-1::-1] = np.add.accumulate(-XexpIntBm[..., ref_index-1::-1]*dz, axis=-1)

    bottom_term = Xref_beta - 2.0 * lidar_ratio * intXexpIntBm

    ba = XexpIntBm / bottom_term - betam 
    ba[...,:start_i] = 0.0
    sigma_a = ba * lidar_ratio

    if apply_on_data:
        data.vars['data'] = sigma_a
        data.desc += ',retrievaled'
    
    return sigma_a.copy()
if __name__ == '__main__':
    pass
