#!/usr/bin/env python
# -*- coding:utf-8 -*-

# fortran_binary.py

import os, sys
#import re
#from datetime import datetime, timedelta
import numpy as np
#import scipy as sp
from scipy.io.numpyio import fread as sp_fread
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#from matplotlib import mlab

class FortranBinary(object):
    def __init__(self, fname, byteswap=False):
        self._f = open(fname, 'rb')
        self._byteswap = 1 if byteswap else 0
        self._rec_num = 0
        self._f.seek(0,2)
        self._filesize = self._f.tell()
        self.rewind()
        while self._f.tell() != self._filesize :
            self._bypass_rec()
            self._rec_num += 1
        self.rewind()

    def __len__(self):
        return self._rec_num

    def read(self, dtype='d', shape=None):
        if self._f.tell() == self._filesize:
            return None
        if dtype in ('d',):
            s = 8
        elif dtype in ('i', 'f'):
            s = 4
        elif dtype in ('s', ):
            s = 2
            #TODO: implement all PyArray types
        rec_len = self._read_rec_len()
        tmp = sp_fread(self._f, rec_len / s, dtype, dtype, self._byteswap)
        if shape is None:
            return tmp
        else:
            return tmp.reshape(shape)

    def _read_rec_len(self):
        rec_len = sp_fread(self._f, 1, 'i', 'i', self._byteswap)[0]
        return rec_len

    def _bypass_rec(self):
        rec_len = self._read_rec_len()
        self._f.seek(rec_len + 4, 1)

    def rewind(self):
        self._f.seek(0, 0)


