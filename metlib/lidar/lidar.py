#!/usr/bin/env python
# -*- coding:utf-8 -*-

# lidar.py
"""class LidarDataset is a container for lidar data.
    TODO: add support for loading short lines.
"""

from datetime import datetime, timedelta
import numpy as np
from netCDF4 import Dataset
from metlib.datetime.datetime_bin import datetime_bin

_std_datetime_fmt = "%Y-%m-%d %H:%M:%S"
_3d_time_channel_bin_varnames = ( ('data', 'f4'),
        )
_1d_time_varnames = ( ('datetime', str),
        ('shots_sum', 'u4'),
        ('trigger_frequency', 'i4'),
#            ('dead_time_corrected', 'u2'),
        ('azimuth_angle', 'f4'),
        ('elevation_angle', 'f4'),
        ('cloud_base_height', 'f4'),
        )
_1d_bin_varnames = ( ('distance', 'f4'),
        )
_2d_time_channel_varnames = ( ('background', 'f4'),
        ('background_std_dev', 'f4'),
        ('energy', 'f4'),
        )
_2d_time_other_varnames = (('temp', 'f4', 'TEMP'), 
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

class LidarDataset(object):
    """Representing Lidar's Dataset"""
    def __init__(self, fnames, bin_num=None, **kwargs):
        """doc
        kwargs:
            fnames: a seq of filenames or a single filename or a str of filenames seperated with comma.
            bin_num: clipping in BIN dimesion when loading files.
        """
        self.orig_fnames = []
        self._vars_inited = False
        self.dims = dict()
        self.dims['BIN'] = bin_num
        self.desc = "No description available"
        self.append_files(fnames, **kwargs)
        if len(self.orig_fnames) != 0:
            f = Dataset(self.orig_fnames[0])
            if 'desc' in f.ncattrs():
                self.desc = "%s" % (f.getncattr('desc'), )
            f.close()
    
    def append_files(self, fnames):
        """append one or more files to the dataset
        fnames: a seq of filenames or a single filename or a str of filenames seperated with comma."""
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
        bin_num = self.dims['BIN']
        if bin_num is None:
            bin_num = orig_bin_nums.min()
        else:
            bin_num = np.min((orig_bin_nums.min(), bin_num))
        proper_dims['BIN'] = bin_num
        proper_dims['TIME'] = record_nums.sum()
        self.dims.update(proper_dims)
        # # create the arrays for each var
        for vname, t in _3d_time_channel_bin_varnames:
            if t is str:
                t = 'O'
            _tmp_pool[vname] = np.zeros((proper_dims['TIME'], proper_dims['CHANNEL'], proper_dims['BIN']), dtype=t)
        for vname, t in _2d_time_channel_varnames:
            if t is str:
                t = 'O'
            _tmp_pool[vname] = np.zeros((proper_dims['TIME'], proper_dims['CHANNEL']), dtype=t)
        for vname, t, dname in _2d_time_other_varnames:
            if t is str:
                t = 'O'
            _tmp_pool[vname] = np.zeros((proper_dims['TIME'], proper_dims[dname]), dtype=t)
        for vname, t in _1d_time_varnames:
            if t is str:
                t = 'O'
            _tmp_pool[vname] = np.zeros((proper_dims['TIME'], ), dtype=t)
        for vname, t in _1d_bin_varnames:
            if t is str:
                t = 'O'
            _tmp_pool[vname] = np.zeros((proper_dims['BIN'], ), dtype=t)
        
        start_is = np.hstack((0, record_nums.cumsum()[:-1]))
        end_is = start_is + record_nums
        for i, fname in enumerate(fnames):
            f = Dataset(fname)
            if i == 0:
                for vname, t in _1d_bin_varnames:
                    _tmp_pool[vname][:] = f.variables[vname][:proper_dims['BIN']]
            for vname, t in _3d_time_channel_bin_varnames:
                _tmp_pool[vname][start_is[i]:end_is[i],:,:] = f.variables[vname][:,:,:proper_dims['BIN']]
            for vname, t in _2d_time_channel_varnames:
                _tmp_pool[vname][start_is[i]:end_is[i],:] = f.variables[vname][:]
            for vname, t, dname in _2d_time_other_varnames:
                _tmp_pool[vname][start_is[i]:end_is[i]] = f.variables[vname][:]
            for vname, t in _1d_time_varnames:
                _tmp_pool[vname][start_is[i]:end_is[i]] = f.variables[vname][:]
            f.close()
 
        _tmp_pool['datetime'] = np.array([datetime.strptime(datestr, _std_datetime_fmt) for datestr in _tmp_pool['datetime']])

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
                self.vars[vname] = np.vstack((self.vars[vname], _tmp_pool[vname]))
            for vname, t in _2d_time_channel_varnames:
                self.vars[vname] = np.vstack((self.vars[vname], _tmp_pool[vname]))
            for vname, t, dname in _2d_time_other_varnames:
                self.vars[vname] = np.vstack((self.vars[vname], _tmp_pool[vname]))
            for vname, t in _1d_time_varnames:
                self.vars[vname] = np.hstack((self.vars[vname], _tmp_pool[vname]))

            self.vars['end_datetime'] = _tmp_pool['end_datetime']
            self.vars['number_records'] += _tmp_pool['number_records']
        self.orig_fnames.extend(fnames)

    def _peek_file_info(self, fname):
        """returns attrs and dim_lens"""
        f = Dataset(fname)
        attrs = dict()
        dim_lens = dict()
        for dimname in f.dimensions:
            dim_lens[dimname] = len(f.dimensions[dimname])
        for attrname in f.ncattrs():
            attrs[attrname] = f.getncattr(attrname)
        attrs['start_datetime'] = datetime.strptime(attrs['start_datetime'], _std_datetime_fmt)
        attrs['end_datetime'] = datetime.strptime(attrs['end_datetime'], _std_datetime_fmt)
        return attrs, dim_lens

    def save(self, fname):
        """Save into a netCDF4 file"""
        f = Dataset(fname, 'w', format='NETCDF4')
        for dname, length in self.dims.items():
            if dname == 'TIME':
                f.createDimension(dname)
            else:
                f.createDimension(dname, length)
        
        for vname, t in _3d_time_channel_bin_varnames:
            f.createVariable(vname, t, ('TIME', 'CHANNEL', 'BIN'))
            f.variables[vname][:] = self.vars[vname]
        for vname, t in _2d_time_channel_varnames:
            f.createVariable(vname, t, ('TIME', 'CHANNEL'))
            f.variables[vname][:] = self.vars[vname]
        for vname, t, dname in _2d_time_other_varnames:
            f.createVariable(vname, t, ('TIME', dname))
            f.variables[vname][:] = self.vars[vname]
        for vname, t, in _1d_time_varnames:
            f.createVariable(vname, t, ('TIME',))
            if vname == 'datetime':
                for i, dt in enumerate(self.vars[vname]):
                    f.variables[vname][i] = dt.strftime(_std_datetime_fmt)
            else:
                f.variables[vname][:] = self.vars[vname]
        for vname, t, in _1d_bin_varnames:
            f.createVariable(vname, t, ('BIN',))
            f.variables[vname][:] = self.vars[vname]
    
        for attr, t in _0d_attrs:
            if attr in ('start_datetime', 'end_datetime'):
                f.setncattr(attr, self.vars[attr].strftime(_std_datetime_fmt))
            else:
                f.setncattr(attr, self.vars[attr])
        f.setncattr('desc', self.desc)
        f.close()

    def time_average(self, tdelta, starttime=None, endtime=None):
        """Averaging in TIME dimesion.
        tdelta is a datetime.timedelta object or an int of minutes.
        starttime and endtime works in the same way as metlib.datetime.datetime_bin.datetime_bin .

        Notice: Some variables are summed instead of averaged. Including:
        data, energy, background, etc.
        """
        if type(tdelta) is not timedelta:
            tdelta = timedelta(minutes=tdelta)
        dts = self.vars['datetime']
        tbins, info = datetime_bin(dts, tdelta, starttime=starttime, endtime=endtime, return_bin_info=True)
        new_time_steps = len(tbins)
        tmp = dict()
        for vname, t in _3d_time_channel_bin_varnames:
            tmp[vname] = np.zeros((new_time_steps, self.dims['CHANNEL'], self.dims['BIN']), dtype=self.vars[vname].dtype)
        for vname, t in _2d_time_channel_varnames:
            tmp[vname] = np.zeros((new_time_steps, self.dims['CHANNEL']), dtype=self.vars[vname].dtype)
        for vname, t, dname in _2d_time_other_varnames:
            tmp[vname] = np.zeros((new_time_steps, self.dims[dname]), dtype=self.vars[vname].dtype)
        for vname, t, in _1d_time_varnames:
            tmp[vname] = np.zeros((new_time_steps, ), dtype=self.vars[vname].dtype)

        for i, w in enumerate(tbins):
            if len(w[0]) == 0:
                flag = True
            else:
                flag = False
            for vname, t, in _1d_time_varnames:
                if vname == 'datetime':
                    tmp[vname][i] = info[i][0]
                elif flag:
                    if t not in ('f4', 'f8', 'd', float):
                        tmp[vname][i] = 0
                    else:
                        tmp[vname][i] = np.nan
                else:
                    if vname in ('shots_sum',):
                    # add , not average. 
                        tmp[vname][i] = self.vars[vname][w].sum(axis=0)
                    else:
                        tmp[vname][i] = self.vars[vname][w].mean(axis=0) 
            for vname, t in _3d_time_channel_bin_varnames:
                if flag:
                    if t not in ('f4', 'f8', 'd', float):
                        tmp[vname][i] = 0
                    else:
                        tmp[vname][i] = np.nan
                else:
                    tmp[vname][i] = self.vars[vname][w].sum(axis=0) 
            for vname, t in _2d_time_channel_varnames:
                if flag:
                    if t not in ('f4', 'f8', 'd', float):
                        tmp[vname][i] = 0
                    else:
                        tmp[vname][i] = np.nan
                else:
                    if vname in ('background', 'energy'):
                        tmp[vname][i] = self.vars[vname].sum(axis=0)
                    elif vname == 'background_std_dev':
                        tmp[vname][i] = np.sqrt(np.mean(self.vars[vname][w] ** 2, axis=0))
                    else:
                        tmp[vname][i] = self.vars[vname][w].mean(axis=0) 
            for vname, t, dname in _2d_time_other_varnames:
                if flag:
                    if t not in ('f4', 'f8', 'd', float):
                        tmp[vname][i] = 0
                    else:
                        tmp[vname][i] = np.nan
                else:
                    tmp[vname][i] = self.vars[vname][w].mean(axis=0) 

        self.vars.update(tmp)
        self.vars['number_records'] = len(tbins)
        self.dims['TIME'] = len(tbins)
    
    def resize_bin(self, start_i, end_i):
        """resize data's BIN dim in python's manner: data[start_i:end_i]
        """
        if end_i > self.vars['number_bins']:
            pass
        else:
            self.vars['data'] = self.vars['data'][:,:,start_i:end_i]
            self.vars['distance'] = self.vars['distance'][start_i:end_i]
            self.vars['number_bins'] = np.max(end_i - start_i, 0)
            self.vars['first_data_bin'] -= start_i

            self.dims['BIN'] = self.vars['number_bins']

    def __str__(self):
        return """    lidarname: %s
    time period: %s - %s
    dims: %s
    vars: %s
    desc: %s
    """ % ( self.vars['lidarname'],
            self.vars['start_datetime'], self.vars['end_datetime'],
            self.dims, 
            self.vars.keys(),
            self.desc)

if __name__ == '__main__':
    pass
