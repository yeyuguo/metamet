#!/usr/bin/env python2.7

# basket.py

import os, sys
import copy
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
from zipfile import ZipFile
from metlib.shell.fileutil import *
from metlib.misc import loadpickle, savepickle, get_ext, strip_ext, str2list

__all__ = [ 'Basket']

class Basket(dict):
    """Basket is a container for collecting variables, to simulate IDL's STORE function.
    """
    def __init__(self, name, scope, varnames=None, tmp_path=None, filename=None, deepcopy=True):
        """
Parameters
----------
name: Basket name.
scope: a dict from which the vars comes and to which the vars goes.
varnames: a list of varnames.
tmp_path: user specified path for storing tmp files. If None: using default ./tmp.basket.BASKETNAME.PID .
filename: if not None, load a stored basket.zip file.
        """
        self.name = name
        self.scope = scope
        self.tmp_path = self.make_tmp(tmp_path)
        self.deepcopy=deepcopy
        if filename is None:
            self.collect(varnames=varnames)
        else:
            self.load(filename, varnames)
        
    def collect(self, varnames=None, source=None, deepcopy=False):
        """
Parameters
----------
varnames: varnames to collect.
source: a dict of vars to collect from. Using globals() as default.
deepcopy: if True, the vars put into the basket are deepcopied, to protect the version in the basket. if None, use the basket's default option, i.e., self.deepcopy .
"""
        if source is None:
            source = self.scope
        if varnames is None:
            varnames = self.keys()
        elif isinstance(varnames, (str, unicode)):
            varnames = str2list(varnames)
        for v in varnames:
            if deepcopy is None:
                deepcopy = self.deepcopy
            if deepcopy:
                self[v] = copy.deepcopy(source.get(v, None))
            else:
                self[v] = source.get(v, None)

    def takeout(self, varnames=None, dest=None, deepcopy=None):
        """
Parameters
----------
varnames: varnames to take to the dest.
dest: a dict as dest of vars. Using globals() as default.
deepcopy: if True, the vars taken out are deepcopied, to protect the version in the basket. if None, use the basket's default option, i.e., self.deepcopy .
"""
        if dest is None:
            dest = self.scope
        if varnames is None:
            varnames = self.keys()
        elif isinstance(varnames, (str, unicode)):
            varnames = str2list(varnames)
        for v in varnames:
            if deepcopy is None:
                deepcopy = self.deepcopy
            if deepcopy:
                dest[v] = copy.deepcopy(self[v])
            else:
                dest[v] = self[v]

    def dump_var(self, varname):
        var = self[varname]
        if isinstance(var, np.ndarray):
            fname = '%s/%s.npy' % (self.tmp_path, varname)
            np.save(fname, var)
        else:
            fname = '%s/%s.pickle' % (self.tmp_path, varname)
            savepickle(fname, var)
        return fname

    def load_var(self, filename):
        ext = get_ext(filename)
        if ext == '.npy':
            var = np.load(filename)
        elif ext == '.pickle':
            var = loadpickle(filename)
        return var

    def make_tmp(self, tmp_path=None):
        if tmp_path in [None, '']:
            tmp_path = './tmp.basket.%s.%d' % (self.name, os.getpid())
        force_makedirs(tmp_path)
        return tmp_path

    def clear_tmp(self):
        force_rm(self.tmp_path)

    def save(self, filename=None, varnames=None):
        if not os.path.exists(self.tmp_path):
            self.make_tmp()
        if filename is None:
            filename = './%s.zip' % self.name

        outflist = []
        if varnames is None:
            varnames = self.keys()
        elif isinstance(varnames, (str, unicode)):
            varnames = str2list(varnames)
        for vname in varnames:
            if vname in self.keys():
                fn = self.dump_var(vname)
                outflist.append(fn)
        force_makedirs(os.path.dirname(filename))
        with ZipFile(filename, 'w') as outzip:
            for fn in outflist:
                outzip.write(fn, os.path.basename(fn))

    def load(self, filename, varnames=None):
        if not os.path.exists(self.tmp_path):
            self.make_tmp()
        with ZipFile(filename) as inzip:
            for fname in inzip.namelist():
                vn = strip_ext(fname)
                if isinstance(varnames, (str, unicode)):
                    varnames = str2list(varnames)
                if varnames is not None and vn not in varnames:
                    continue
                extract_fname = '%s/%s' % (self.tmp_path, fname)
                inzip.extract(fname, self.tmp_path)
                var = self.load_var(extract_fname)
                self[vn] = var

    def close(self):
        self.clear()
        self.clear_tmp()

    def __str__(self):
        sss = "Basket: %s \n"  % (self.name, )
        vss = []
        for v in self.keys():
            vstr = str(self[v])
            if len(vstr) > 32:
                short_vstr = '%s...' % vstr[0:29]
            else:
                short_vstr = '%-32s' % vstr
            vss.append(' %-8s : %s , %s' % (v, short_vstr, type(self[v])))
        sss = sss + '\n'.join(vss) 
        return sss
    
    def __repr__(self):
        return self.__str__()

if __name__ == '__main__':
    a = 5
    s = 'abc'
    b = np.random.rand(5,3)
    basket = Basket('MyBasket', globals(), ['a', 'b', 's'])
    print basket
    basket.save()
    basket.close()
    b2 = Basket('B2', globals(), filename='./MyBasket.zip', varnames=['a', 'b'])
    print b2
    b2.save('B2.zip')
    b2.close()
