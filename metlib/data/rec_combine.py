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
    def _rec_from_seqs_seqs_shape_error():
        raise AssertionError("rec_from_seqs: len(names): %d does not fit to seqs.shape: %s" % (len(names), seqs.shape))

    if isinstance(seqs, np.ndarray):
        # in order that the following for seq in seqs is valid
        if len(seqs.shape) == 1:
            if len(names) == 1:
                seqs = seqs[np.newaxis, :]
            elif len(names) == len(seqs):
                seqs = seqs[:, np.newaxis]
                sys.stderr.write("Warning: rec_from_seqs: seqs is an 1d array, treating as several individual numbers since len(names) is exactly the same as len(seqs). \n")
            else:
                _rec_from_seqs_seqs_shape_error()
        elif len(seqs.shape) == 2:
            if seqs.shape[1] == len(names):
                seqs = seqs.transpose() 
            elif seqs.shape[0] == len(names):
                sys.stderr.write("Warning: rec_from_seqs: seqs is an 2d array with shape of %s, but len(names) is %d . Using rows of seqs as fields of the recarray. \n" % (seqs.shape, len(names)))
            else:
                _rec_from_seqs_seqs_shape_error()
        else:
            raise RuntimeError("rec_from_seqs: since seqs is np.ndarray, it should be 1d or 2d, but the given seqs.shape is %s" % seqs.shape)
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
    e = np.random.rand(7, 3)
    f = np.random.rand(3, 10)
    g = np.random.rand(3, 3)
    h = np.random.rand(5, 6)
    k = np.random.rand(3)
    l = np.random.rand(3, 1)
    m = np.random.rand(1, 3)

    names = ('datetime', 'a', 'c', )

    r1 = rec_from_seqs(names, (d, a, c))
    print r1.dtype
    print r1
    print np.hstack((r1, r1))

    print "--- using ndarray as seqs ---"
    print 'len(names): 3'
    print "seqs: (7, 3)"
    print rec_from_seqs(names, e)
    print "seqs: (3, 10)"
    print rec_from_seqs(names, f)
    print "seqs: (3, 3)"
    print rec_from_seqs(names, g)
#    print "seqs: (5, 6)"
#    print rec_from_seqs(names, h)
    print "seqs: (3,)"
    print rec_from_seqs(names, k)
    print "seqs: (3, 1)"
    print rec_from_seqs(names, l)
    print "seqs: (1, 3)"
    print rec_from_seqs(['a'], m).dtype


