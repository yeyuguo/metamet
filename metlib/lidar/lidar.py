#!/usr/bin/env python
# -*- coding:utf-8 -*-

# lidar.py
"""class LidarDataset is a container for lidar data.
    TODO: add support for loading short lines.
    TODO: make 'must'/'optional' work
"""

from datetime import datetime, timedelta
from copy import copy, deepcopy
import numpy as np
from netCDF4 import Dataset, date2num, num2date
from metlib.datetime.datetime_bin import datetime_bin

__all__ = ['LidarDataset']
_std_datetime_fmt = "%Y-%m-%d %H:%M:%S"
_std_datetime_units = "seconds since 1970-01-01 00:00:00"
_NO_DESC_STR = "No description available"
# # Table driven:
# # varname, format, dim shape, 'must'/'optional', average method
_varnames = (
        ('data', 'f4', ('TIME', 'CHANNEL', 'BIN'), 'must', 'sum'),
        ('datetime', str, ('TIME',), 'must', 'special'),
        ('shots_sum', 'u4', ('TIME',), 'optional', 'sum'),
        ('trigger_frequency', 'i4', ('TIME', ), 'optional', 'mean'),
        ('dead_time_corrected', 'u2', ('TIME', ), 'optional', 'first'),
        ('azimuth_angle', 'f4', ('TIME', ), 'optional', 'mean'),
        ('elevation_angle', 'f4', ('TIME',), 'optional', 'mean'),
        ('cloud_base_height', 'f4', ('TIME',), 'optional', 'mean'),
        ('cloud_base_height1', 'f4', ('TIME',), 'optional', 'mean'),
        ('cloud_base_height2', 'f4', ('TIME',), 'optional', 'mean'),
        ('cloud_base_height3', 'f4', ('TIME',), 'optional', 'mean'),
        ('cloud_base_height4', 'f4', ('TIME',), 'optional', 'mean'),
        ('distance', 'f4', ('BIN',), 'must', 'special'),
        ('background', 'f4', ('TIME', 'CHANNEL'), 'must', 'sum'),
        ('background_std_dev', 'f4', ('TIME', 'CHANNEL'), 'optional', 'sqr_mean_sqrt'),
        ('energy', 'f4', ('TIME', 'CHANNEL'), 'must', 'sum'),
        ('temp', 'f4', ('TIME','TEMP'), 'optional', 'mean'),
        )
_attrs = (
        ('lidarname', str, 'must'),
        ('bin_time', 'f4', 'must'),
        ('bin_size', 'f4', 'must'),
        ('first_data_bin', 'i4', 'must'),
        ('start_datetime', str, 'must'),
        ('end_datetime', str, 'must'),
        ('number_records', 'i4', 'must'),
        ('number_bins', 'i4', 'must'),
        ('number_channels', 'i4', 'must'),
        ('data_aver_method', str, 'optional'),
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
        self._used_var_names = set()
        self._used_attr_names = set()
        self.dims = dict()
        self.dims['BIN'] = bin_num
        self.desc = _NO_DESC_STR
        self.append_files(fnames, **kwargs)
        if len(self.orig_fnames) != 0:
            f = Dataset(self.orig_fnames[0])
            if 'desc' in f.ncattrs():
                self.desc = "%s" % (f.getncattr('desc'), )
            if 'data_aver_method' not in f.ncattrs():
                self.vars['data_aver_method'] = 'sum'
                self._used_attr_names.add('data_aver_method')
            f.close()

    def copy(self):
        return deepcopy(self)

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
            del attrs
            del dim_lens
        bin_num = self.dims['BIN']
        if bin_num is None:
            bin_num = orig_bin_nums.min()
        else:
            bin_num = np.min((orig_bin_nums.min(), bin_num))
        proper_dims['BIN'] = bin_num
        proper_dims['TIME'] = record_nums.sum()
        self.dims.update(proper_dims)
        # # create the arrays for each var
        for vname, t, dimnames, choice, aver_method in _varnames:
            if t is str:
                t = 'O'
            _tmp_pool[vname] = np.zeros(tuple([proper_dims[d] for d in dimnames]), dtype=t)

        start_is = np.hstack((0, record_nums.cumsum()[:-1]))
        end_is = start_is + record_nums
        for i, fname in enumerate(fnames):
            f = Dataset(fname)
            
            for vname, t, dimnames, choice, aver_method in _varnames:
                if choice is 'optional' and vname not in f.variables:
                    continue
                else:
                    self._used_var_names.add(vname)
                if dimnames == ('BIN',):
                    if i == 0:
                        _tmp_pool[vname][:] = f.variables[vname][:proper_dims['BIN']]
                elif 'BIN' in dimnames:
                    _tmp_pool[vname][start_is[i]:end_is[i]] = f.variables[vname][:, ... ,:proper_dims['BIN']]
                else:
                    _tmp_pool[vname][start_is[i]:end_is[i]] = f.variables[vname][:]
            f.close()
        datetime_type = type(_tmp_pool['datetime'][0])
        if datetime_type == np.string_ or datetime_type == str:
            _tmp_pool['datetime'] = np.array([datetime.strptime(datestr, _std_datetime_fmt) for datestr in _tmp_pool['datetime']])
        else:
            _tmp_pool['datetime'] = num2date(_tmp_pool['datetime'], units=_std_datetime_units)

        for attr in ref_attrs.keys():
            self._used_attr_names.add(attr)
            _tmp_pool[attr] = ref_attrs[attr]
        _tmp_pool['start_datetime'] = all_start_datetime
        _tmp_pool['end_datetime'] = all_end_datetime
        _tmp_pool['number_bins'] = proper_dims['BIN']
        _tmp_pool['number_records'] = proper_dims['TIME']
        if not self._vars_inited:
            self.vars = _tmp_pool
            self._vars_inited = True
        else:
            for vname, t, dimnames, choice, aver_method in _varnames:
                if 'TIME' not in dimnames:
                    continue
                if len(dimnames) > 1:
                    self.vars[vname] = np.vstack((self.vars[vname], _tmp_pool[vname]))
                else:
                    self.vars[vname] = np.hstack((self.vars[vname], _tmp_pool[vname]))
            self.vars['end_datetime'] = _tmp_pool['end_datetime']
            self.vars['number_records'] += _tmp_pool['number_records']
        del _tmp_pool
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
        f.close()
        return attrs, dim_lens

    def save(self, fname, use_datetime_str=True):
        """Save into a netCDF4 file"""
        f = Dataset(fname, 'w', format='NETCDF4')
        for dname, length in self.dims.items():
            if dname == 'TIME':
                f.createDimension(dname)
            else:
                f.createDimension(dname, length)
        for vname, t, dimnames, choice, aver_method in _varnames:
            if vname not in self._used_var_names:
                continue
            if vname == 'datetime':
                if use_datetime_str:
                    f.createVariable(vname, t, dimnames)
                    for i, dt in enumerate(self.vars[vname]):
                        f.variables[vname][i] = self.vars[vname][i].strftime(_std_datetime_fmt)
                else:
                    f.createVariable(vname, 'i4', dimnames)
                    f.variables[vname].setncattr('units', _std_datetime_units)
                    f.variables[vname][:] = date2num(self.vars[vname], _std_datetime_units)
            else:
                f.createVariable(vname, t, dimnames)
                f.variables[vname][:] = self.vars[vname]
    
        for attr in self._used_attr_names:
            if isinstance(self.vars[attr], datetime):
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

        for vname, t, dimnames, choice, aver_method in _varnames:
            if 'TIME' not in dimnames:
                continue
            new_shape = [self.dims[d] for d in dimnames]
            new_shape[0] = new_time_steps
            tmp[vname] = np.zeros(tuple(new_shape), dtype=self.vars[vname].dtype)

        for i, w in enumerate(tbins):
            for vname, t, dimnames, choice, aver_method in _varnames:
                if 'TIME' not in dimnames:
                    continue
                if vname == 'datetime':
                    # # using each tbins' starttime as datetime
                    tmp[vname][i] = info[i][0]
                elif vname == 'data':
                    if self.vars['data_aver_method'] == 'sum':
                        tmp[vname][i] = self.vars[vname][w].sum(axis=0)
                    elif self.vars['data_aver_method'] == 'mean':
                        tmp[vname][i] = self.vars[vname][w].mean(axis=0)
                    else:
                        sys.stderr.write('Lidar data average method: %s not implemented\n' % self.vars['data_aver_method'])
                elif len(w[0]) == 0:
                    # # filling with nan or 0
                    if t not in ('f4', 'f8', 'd', 'g', float, np.float32, np.float64, np.float_, np.single, np.double):
                        tmp[vname][i] = 0
                    else:
                        tmp[vname][i] = np.nan
                else:
                    if aver_method == 'sum':
                        tmp[vname][i] = self.vars[vname][w].sum(axis=0)
                    elif aver_method == 'mean':
                        tmp[vname][i] = self.vars[vname][w].mean(axis=0)
                    elif aver_method == 'first':
                        tmp[vname][i] = self.vars[vname][w][0]
                    elif aver_method == 'sqr_mean_sqrt':
                        # # for std_dev 
                        tmp[vname][i] = np.sqrt(np.mean(self.vars[vname][w] ** 2, axis=0))
        self.vars.update(tmp)
        self.recheck_time()

    def __len__(self):
        return self.dims['TIME']

    def recheck_time(self):
        """recheck stuffs about time dimension"""
        n_tbins = len(self.vars['datetime'])
        self.vars['start_datetime'] = self.vars['datetime'][0]
        self.vars['end_datetime'] = self.vars['datetime'][-1] + timedelta(seconds = int(self.vars['shots_sum'][-1] / self.vars['trigger_frequency'][-1]))
        self.vars['number_records'] = n_tbins
        self.dims['TIME'] = n_tbins

    def get_timedeltas(self, return_seconds=True):
        """Get array of each record's time span. 
        if return_seconds is True: return in seconds
        else: return in timedelta objects.
        """
        seconds = (self.vars['shots_sum'] / self.vars['trigger_frequency']).astype('i8')
        if return_seconds:
            return seconds
        else:
            tds = np.array([timedelta(seconds = int(s)) for s in seconds])
            return tds

    def get_end_datetimes(self):
        """Get array of each record's end datetimes"""
        tds = self.get_timedeltas(return_seconds=False)
        return self.vars['datetime'] + tds

    def get_mid_datetimes(self):
        """Get array of each record's mid datetimes"""
        tds = self.get_timedeltas(return_seconds=False)
        return self.vars['datetime'] + tds / 2


    def trim_period(self, starttime, endtime):
        """Trim unwanted data, leaving data between start_time and end_time only.
        """
        dts = self.vars['datetime']
        tbins, info = datetime_bin(dts, None, starttime=starttime, endtime=endtime, return_bin_info=True)
        choosen_w = tbins[0]
        new_time_steps = len(tbins[0][0])
        tmp = dict()
        for vname, t, dimnames, choice, aver_method in _varnames:
            if 'TIME' not in dimnames:
                continue
            tmp[vname] = self.vars[vname][choosen_w]

        self.vars.update(tmp)
        self.recheck_time()

    def __getitem__(self, key):
        """return a new LidarDataset object that contains the slice (in TIME dimension) if key is slice or integer. 
        return corresponding data if key is str
        """
        if isinstance(key, slice):
            new_data = self.copy()
            for vname, t, dimnames, choice, aver_method in _varnames:
                if 'TIME' not in dimnames:
                    continue
                new_data.vars[vname] = new_data.vars[vname][key]
            new_data.recheck_time()
            return new_data
        elif isinstance(key, (int, long, np.integer)):
            new_data = self.copy()
            for vname, t, dimnames, choice, aver_method in _varnames:
                if 'TIME' not in dimnames:
                    continue
                new_data.vars[vname] = np.array(new_data.vars[vname][key])[np.newaxis, ...]
            new_data.recheck_time()
            return new_data
        elif isinstance(key, (str, unicode)):
            return self.vars[key]

    def __setitem__(self, key, value):
        if isinstance(key, (str, unicode)):
            self.vars[key] = value
            self._used_attr_names.add(key)
        else:
            sys.stderr.write('Warning: key is not str, not setting LidarDataset property\n')
            
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
    desc: %s
    time period: %s - %s
    dims: %s
    vars: %s
    """ % ( self.vars['lidarname'],
            self.desc,
            self.vars['start_datetime'], self.vars['end_datetime'],
            self.dims, 
            self.vars.keys(),
            )

    def __repr__(self):
        return self.__str__()
    
if __name__ == '__main__':
    pass
