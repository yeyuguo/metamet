#!/usr/bin/env python
# -*- coding:utf-8 -*-

# lookup_table.py

import os, sys
import numpy as np
import scipy as sp

class lookup_table(object):
    def __init__(self, arr, dims):
        """arr is the big ndarray of lookup_table,
        dims is a list of name, values tuple:
        [('dim1',[0.1,0.2,0.3,0.4,0.5]), ('dim2',[35.,40.,50.]),...]
        """
        self.arr = arr
        # # check
        shape_checker = []
        for d in dims:
            shape_checker.append(len(d[1]))
            l = list(d[1])
            order_checker = sorted(l)
            if l != order_checker and l != reversed(order_checker):
                raise ValueError( \
"""Lookup Table's dim: %s is not in ascending or descending order
    %s
""" % (d[0], d[1]) )
        if tuple(shape_checker) != self.arr.shape:
            raise ValueError("Lookup Table's array and dim mismatch: %s vs %s" \
                    % (self.arr.shape, tuple(shape_checker)))

        self.dims = dims
        self.dimnames = [item[0] for item in dims]
        

    def lookup(self, **kwargs):
        """lt.lookup(dim1=?.?, dim2=?.?,..., dimn=?.?)
        if len(dims) - len(kwargs) == 1, return a scaler value, 
        else, return a lookup_table with len(dims) - len(kwargs) dims.
        """
        print kwargs
        order = []
        for name in self.dimnames:
            if name in kwargs:
                order.append(name)

        # # TODO: add check with self.dims and length check and range check
        if len(order) != len(kwargs):
            raise ValueError("""Dim names not match.
    Lookup Table's dim names: %s
    Function args: %s""" % ( self.dimnames, kwargs.keys() ) )


        
        # # get enough good info
        good_info = dict()
        for now_dimname in order:
            # find dim's index in all dim
            for i, dim in enumerate(self.dims):
                if now_dimname == dim[0]:
                    dim_i = i
                    dim_value = np.array(dim[1])
                    break
            now_value = kwargs[now_dimname]
            # # To prevent extrapolating
            if now_value < dim_value.min():
                now_value = dim_value.min()
            elif now_value > dim_value.max():
                now_value = dim_value.max()

            # find layer's index in the dim
            for i in range(len(dim_value)-1):
                if (dim_value[i]<=now_value and now_value<=dim_value[i+1]) \
                    or \
                    (dim_value[i]>=now_value and now_value>=dim_value[i+1]):
                    left_i, right_i = i, i+1
                    break
            left_value, right_value = dim_value[i], dim_value[i+1]
            left_ratio = (right_value - now_value) / (right_value - left_value)
            right_ratio = (now_value - left_value) / (right_value - left_value)
            good_info[now_dimname] = {'dimname':now_dimname, 'dim_i':dim_i, \
                    'left_i':left_i, 'right_i':right_i, \
                    'left_ratio':left_ratio, 'right_ratio':right_ratio }
        # # make a small array for interp
        magic = 'self.arr['
        for dimname in self.dimnames:
            if dimname not in good_info:
                magic += ':,'
            else:
                info = good_info[dimname]
                magic += '%d:%d,' % (info['left_i'], info['right_i']+1)
        magic = magic.rstrip(',') + ']'
        small_arr = eval(magic)
        for dimname in order:
            info = good_info[dimname]
            if len(small_arr.shape) > 1:
                small_arr = small_arr[0,:] * info['left_ratio'] + \
                        small_arr[1,:] * info['right_ratio']
            else:
                small_arr = small_arr[0] * info['left_ratio'] + \
                        small_arr[1] * info['right_ratio']

        if len(order) == len(self.dimnames):
            # in this case, small_arr is already a scaler
            return small_arr
        else:
            # make a smaller lookup_table
            new_dims = []
            for d in self.dims:
                if d[0] not in order:
                    new_dims.append(d)
            return lookup_table(small_arr, new_dims)


if __name__ == '__main__':
    dim1 = np.arange(0.1,0.51,0.1)
    dim2 = np.array([35,40,50])
    lt_arr = np.arange(len(dim1)*len(dim2)).reshape((len(dim1),len(dim2)))
    lt = lookup_table(lt_arr, [('dim1',dim1), ('dim2',dim2)])
    print dim1, dim2
    print lt_arr
    res1 = lt.lookup(dim1=0.6, dim2=45.0)
    res2 = lt.lookup(dim1=0.35)
    print res1
    print res2.arr
    print res2.dims
    res3 = res2.lookup(dim3=45.0)
    print res3


