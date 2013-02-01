#!/usr/bin/env python

# misc.py

import os
import re
import pickle
#from datetime import datetime, timedelta
#from dateutil.parser import parse
import numpy as np
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#from matplotlib import mlab
#from netCDF4 import Dataset

__all__ = ['grep', 'strip_ext', 'sub_ext', 'get_ext', 'savepickle', 'loadpickle']

def grep(pattern, seq, flags=0):
    """grep greps patterns from seqs.
Parameters:
    pattern: regex pattern str or compiled regex pattern or func. 
    seq: seq of str or any other stuffs, etc. If pattern is not func and seq[0] is not str/unicode, seq will be converted using str() first.
    flags: 'ILMSUX' or number of re.I|re.L|re.M|re.S|re.U|re.X .
        I: ignore case;
        L: locale dependent;
        M: multi-line;
        S: dot matches all;
        U: unicode dependent;
        X: verbose.
Returns:
    A filtered list.
    """
    if isinstance(flags, (str, unicode)):
        true_flags = 0
        flags = flags.upper()
        for letter in flags:
            if letter in 'ILMSUX':
                true_flags += re.__dict__[letter]
    else:
        true_flags = flags
    if isinstance(pattern, (str, unicode, type(re.compile(r'')) ) ):
        res = []
        seq = [str(item) for item in seq]
        for item in seq:
            if re.search(pattern, item, true_flags):
                res.append(item)
    elif callable(pattern):
        res = filter(pattern, seq)

    return res

def strip_ext(path):
    """strips .ext from a path"""
    return os.path.splitext(path)[0]

def get_ext(path):
    """get .ext from a path"""
    return os.path.splitext(path)[1]

def sub_ext(orig, new_ext):
    """sub .ext with a new one"""
    if not new_ext.startswith('.'):
        new_ext = '.' + new_ext
    return strip_ext(orig) + new_ext

def savepickle(fname, obj):
    outf = open(fname, 'w')
    pickle.dump(obj, outf)
    outf.close()

def loadpickle(fname):
    infile = open(fname)
    obj = pickle.load(infile)
    infile.close()
    return obj


if __name__ == '__main__':
    l = ['abcde', 'asldkfj', 'sdjfowij', 'sdfoijw', '1243450', '1204023']
    print grep(re.compile('sd'), l)
    print grep(r"^\d*$", l)
    print grep(lambda s: s.startswith('a'), l)
    p = 'abc/def/gh.hi.sf'
    print strip_ext(p)
    print get_ext(p)
    print sub_ext(p, 'txt')
