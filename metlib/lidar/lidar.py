#!/usr/bin/env python
# -*- coding:utf-8 -*-

# lidar.py
"""class LidarDataset is a container for lidar data.
    TODO: add support for loading short lines.
"""

import os, sys
#import re
from datetime import datetime, timedelta
import numpy as np
#import scipy as sp
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#from matplotlib import mlab
from netCDF4 import Dataset

class LidarDataset(object):
    """doc"""
    _std_datetime_fmt = "%Y-%m-%d %H:%M:%S"
    _3d_time_channel_bin_varnames = ( ('data', 'f4'),
            )
    _1d_time_varnames = ( ('datetime', str),
            ('distance', 'f4'),
            ('shots_sum', 'u4'),
            ('trigger_frequency', 'i4'),
#            ('dead_time_corrected', 'u2'),
            ('azimuth_angle', 'f4'),
            ('elevation_angle', 'f4'),
            ('cloud_base_height', 'f4'),
            )
    _2d_time_channel_varnames = ( ('background', 'f4'),
            ('background_std_dev', 'f4'),
            ('energy', 'f4'),
            )
    _2d_time_other_varnames = (('temp', 'f4'), 
            )
    _0d_attrs = ( ('lidarname', str),
            ('bin_time', 'f4'),
            ('bin_size', 'f4'),
            ('first_data_bin', 'i4'),
            ('start_datetime', str),
            ('end_datetime', str),
            ('number_records', 'i4'),
            ('number_bins', 'i4'),
            ('number_channels', 'i4'),
            )
    def __init__(self, fnames, **kwargs):
        """doc
        kwargs:
            bin_num
        """
        self.orig_fnames = []
        self._vars_inited = False
        self.append_files(fnames, **kwargs)
    
    def append_files(self, fnames, bin_num=None):
        _tmp_pool = dict()
        if type(fnames) is str:
            fnames = fnames.split(',')
        self.orig_fnames.extend(fnames)
        record_nums = np.zeros(len(fnames), dtype='i4')
        orig_bin_nums = np.zeros(len(fnames), dtype='i4')
        

        for i, fname in enumerate(fnames):
            attrs, dim_lens = self._peek_file_info(fname)
            record_nums[i] = dim_lens['TIME']
            orig_bin_nums[i] = dim_lens['BIN']
            if i == 0:
                proper_dims = dim_lens
                ref_attrs = attrs
                all_start_datetime = attrs['start_datetime']
            if i == len(fnames) - 1:
                all_end_datetime = attrs['end_datetime']

        if bin_num is None:
            bin_num = orig_bin_nums.min()
        else:
            bin_num = np.min((orig_bin_nums.min(), bin_num))
        proper_dims['BIN'] = bin_num
        proper_dims['TIME'] = record_nums.sum()
        
        # # create the arrays for each var
        for vname, t in _3d_time_channel_bin_varnames:
            if t is str:
                t = 'O'
            _tmp_pool[vname] = np.zeros((proper_dims['TIME'], proper_dims['CHANNEL'], proper_dims['BIN']), dtype=t)
        for vname, t in _2d_time_channel_varnames:
            if t is str:
                t = 'O'
            _tmp_pool[vname] = np.zeros((proper_dims['TIME'], proper_dims['CHANNEL']), dtype=t)
        for vname, t in _2d_time_other_varnames:
            if t is str:
                t = 'O'
            # # TODO: how to deal with this?
        for vname, t in _1d_time_varnames:
            if t is str:
                t = 'O'
            _tmp_pool[vname] = np.zeros((proper_dims['TIME'], ), dtype=t)
        
        end_is = record_nums.cumsum()
        start_is = end_is - record_nums[0]
        for i, fname in enumerate(fnames):
            f = Dataset(fname)
            for vname, t in _3d_time_channel_bin_varnames:
                _tmp_pool[vname][start_is[i]:end_is[i],:,:] = f.variables[vname][:,:,:proper_dims['BIN']]
            for vname, t in _2d_time_channel_varnames:
                _tmp_pool[vname][start_is[i]:end_is[i],:] = f.variables[vname][:]
            for vname, t in _2d_time_other_varnames:
                #_tmp_pool[vname][start_is[i]:end_is[i],:] = f.variables[vname][:]
                #TODO
                pass
            for vname, t in _1d_time_varnames:
                _tmp_pool[vname][start_is[i]:end_is[i]] = f.variables[vname][:]
            f.close()
        for attr, t in _0d_attrs:
            _tmp_pool[attr] = ref_attrs[attr]
        _tmp_pool['start_datetime'] = all_start_datetime
        _tmp_pool['end_datetime'] = all_end_datetime
        _tmp_pool['number_bins'] = proper_dims['BIN']
        _tmp_pool['number_records'] = proper_dims['TIME']
        if not self._vars_inited:
            self.vars = _tmp_pool
            self._vars_inited = True
        else:
            for vname, t in _3d_time_channel_bin_varnames:
                self.vars[vname] = np.vstack(self.vars[vname], _tmp_pool[vname])
            for vname, t in _2d_time_channel_varnames:
                self.vars[vname] = np.vstack(self.vars[vname], _tmp_pool[vname])
            for vname, t in _2d_time_other_varnames:
#                self.vars[vname] = np.vstack(self.vars[vname], _tmp_pool[vname])
            #   TODO
                pass
            for vname, t in _1d_time_varnames:
                self.vars[vname] = np.hstack(self.vars[vname], _tmp_pool[vname])
            self.vars['end_datetime'] = _tmp_pool['end_datetime']
            self.vars['number_records'] += _tmp_pool['number_records']

    def _peek_file_info(self, fname):
        """returns attrs and dim_lens"""
        f = Dataset(fname)
        attrs = dict()
        dim_lens = dict()
        for dimname in f.dimensions:
            dim_lens[dimname] = len(f.dimensions[dimname])
        for attrname in f.ncattrs():
            attrs[attrname] = f.getncattr(attrname)
        attrs[start_datetime] = datetime.strptime(attrs[start_datetime], _std_datetime_fmt)
        attrs[end_datetime] = datetime.strptime(attrs[end_datetime], _std_datetime_fmt)
        return attrs, dim_lens

    def save(self, fname):
        """doc"""
        pass


if __name__ == '__main__':
    pass
