#!/usr/bin/env python

# data_bin.py
"""This module provides functions on binning and averaging data"""

import os, sys
import numpy as np

__all__ = ['data_bin'] 
def data_bin(data, binsize, start=None, end=None, return_where=False, return_bin_info=False):
    """This function partitions a seq of data into equal bin. 

    Return rules:
    If return_where is False (default):
        Returns a list of binned data array.
    Else:
        Returns a list of np.where tuples.
    If return_bin_info is True:
        also returns a list of (bin_start, bin_end) tuples

    Parameters:
    data: a seq of data.
    binsize: binsize.  
    start is a value or None. If it's None, use the first value in the input sequence as start.
    end is a value or None. If it's None, use the last value + 0.5 * binsize in the input sequence as end.
    return_where & return_bin_info:
        see return rules above
    """
    if len(data) == 0:
        if return_bin_info:
            return [], []
        else:
            return []
    if start is None:
        start = data[0]
    if end is None:
        end = data[-1] + binsize * 0.5
    else:
        end = end + binsize * 0.001

    split_points = np.arange(start, end, binsize)
    start_points = split_points[:-1]
    end_points   = split_points[1:]
    d_result = []
    w_result = []
    bin_info = []
    for bi in range(len(start_points)):
        w = np.where( (data>=start_points[bi]) & (data<end_points[bi]) )
        w_result.append(w)
        d_result.append(data[w])
        bin_info.append((start_points[bi], end_points[bi]))
    
    if return_where:
        result = w_result
    else:
        result = d_result

    if return_bin_info is True:
        return result, bin_info
    else:
        return result


if __name__ == '__main__':
    a = np.random.rand(100)
    b, i = data_bin(a, 0.1, 0.0, 1.0, return_bin_info=True)
    w = data_bin(a, 0.2, 0.0, 1.0, return_where=True)
    print b, i
    print w
