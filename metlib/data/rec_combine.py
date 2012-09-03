#!/usr/bin/env python2.7

# rec_combine.py

import os, sys
#import re
#from datetime import datetime, timedelta
#from dateutil.parser import parse
import numpy as np
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#from matplotlib import mlab
#from netCDF4 import Dataset

__all__ = ['rec_from_seqs']

def rec_from_seqs(names, seqs, dtypes=None):
    """Generates recarray from individual seqs.
    Parameters:
        names: names of each seq;
        seqs: the seqs to combine;
        dtypes: dtypes of each seq. If None: try to deduce them from the seqs.
    Returns:
        a recarray.
    """
    seqs = [np.array(seq) for seq in seqs]
    if dtypes is None:
        dtypes = [seq.dtype for seq in seqs]
    try:
        assert len(names) == len(seqs) == len(dtypes)
    except AssertionError as e:
        raise AssertionError('Lengths of names, seqs and dtypes are not equal: [%d %d %d]' % (len(names), len(seqs), len(dtypes)))
    lens = np.array([len(seq) for seq in seqs])
    lensdiff = np.abs(lens - lens[0])
    try:
        assert not np.any(lensdiff)
    except AssertionError as e:
        raise AssertionError('Length of each seq is not equal: %s' % str(lens) )
    rec_dtype = np.dtype(zip(names, dtypes))
    rec = np.zeros(len(seqs[0]), dtype=rec_dtype)
    for i in range(len(seqs)):
        rec[names[i]] = seqs[i]
    return rec


if __name__ == '__main__':
    from metlib.datetime import *
    a = np.random.rand(7)
    b = np.random.rand(7)
    c = [1,2,3,4,5,6,7]
    d = T([20010101, 20020101, 20030101, 20040101, 20050101, 20060101, 20070101])

    names = ('datetime', 'a', 'c', )

    r1 = rec_from_seqs(names, (d, a, c))
    print r1.dtype
    print r1
    print np.hstack((r1, r1))
