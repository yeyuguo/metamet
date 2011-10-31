#!/usr/bin/env python
# -*- coding:utf-8 -*-

# calmet.py

import os, sys
#import re
#from datetime import datetime, timedelta
import numpy as np
#import scipy as sp
#from scipy.io.numpyio import fread as sp_fread
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#from matplotlib import mlab

#__all__ = ['CalmetDataset']


_CalmetControlParas = [
        ('IBYR','i4'),('IBMO','i4'),('IBDY','i4'),
        ('IBHR','i4'),('IBSEC','i4'),
        ('IEYR','i4'),('IEMO','i4'),('IEDY','i4'),
        ('IEHR','i4'),('IESEC','i4'),('AXTZ','S8'),
        ('IRLG','i4'),('IRTYPE','i4'),
        ('NX','i4'),('NY','i4'),('NZ','i4'),
        ('DGRID','f4'),('XORIGR','f4'),('YORIGR','f4'), 
        ('IWFCOD','i4'),('NSSTA','i4'),
        ('NUSTA','i4'),('NPSTA','i4'),('NOWSTA','i4'),('NLU','i4'),
        ('IWAT1','i4'),('IWAT2','i4'),('LCALGRD','i4'),
        ('PMAP','S8'),('DATUM','S8'),('DATEN','S12'),
        ('FEAST','f4'),('FNORTH','f4'),('UTMHEM','S4'),('IUTMZN','i4'),
        ('RNLAT0','f4'),('RELON0','f4'),('XLAT1','f4'),('XLAT2','f4') 
        ]
_CalmetCellFaceHeights = [
        ('CLAB1','S8'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),['ZFACEM','(%(NCELLFACE)d,)f4']
        ]
_CalmetXYSurfStations1 = [
        ('CLAB2','S8'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),['XSSTA','(%(NSSTA)d,)f4']
        ]
_CalmetXYSurfStations2 = [
        ('CLAB3','S8'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),['YSSTA','(%(NSSTA)d,)f4']
        ]
_CalmetXYUpperStations1 = [
        ('CLAB4','S8'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),['XUSTA','(%(NUSTA)d,)f4'],
        ]
_CalmetXYUpperStations2 = [
        ('CLAB5','S8'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),['YUSTA','(%(NUSTA)d,)f4']
        ]
_CalmetXYPrecStations1 = [
        ('CLAB6','S8'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),['XPSTA','(%(NPSTA)d,)f4']
        ]
_CalmetXYPrecStations2 = [
        ('CLAB7','S8'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),['YPSTA','(%(NPSTA)d,)f4']
        ]
_CalmetSurfRough = [
        ('CLAB8','S8'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),['Z0','(%(NY)d, %(NX)d)f4']
        ]
_CalmetLanduse = [
        ('CLAB9','S8'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),['ILANDU','(%(NY)d, %(NX)d)i4']
        ]
_CalmetElev = [
        ('CLAB10','S8'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),['ELEV','(%(NY)d, %(NX)d)f4']
        ]
_CalmetLeafAreaIndex = [
        ('CLAB11','S8'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),['XLAI','(%(NY)d, %(NX)d)f4']
        ]
_CalmetNearestSurfStationNo = [
        ('CLAB12','S8'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),('IDUM','i4'),['NEARS','(%(NY)d, %(NX)d)i4']
        ]

class CalmetDataset(object):
    def __init__(self, fname):
        self.fname = fname
        self._f = open(fname, 'rb')
        # Get file size
        self._f.seek(0,2)
        self._filesize = self._f.tell()

        now_pos = 0
        self.rec1, now_pos = self._read_record(now_pos, 'S' )
        self.NCOM, now_pos = self._read_record(now_pos, 'i4')
        self.COMMENT = []
        for i in range(self.NCOM):
            comment, now_pos = self._read_record(now_pos, 'S')
            self.COMMENT.append(comment)
        tmp, now_pos = self._read_record(now_pos, 'S', convert_type=_CalmetControlParas, add_to_dataset=True)
        self.NCELLFACE = self.NZ + 1
        tmp, now_pos = self._read_record(now_pos, 'S', convert_type=_CalmetCellFaceHeights, add_to_dataset=True)

        if self.NSSTA >= 1:
            tmp, now_pos = self._read_record(now_pos, 'S', convert_type=_CalmetXYSurfStations1, add_to_dataset=True)
            tmp, now_pos = self._read_record(now_pos, 'S', convert_type=_CalmetXYSurfStations2, add_to_dataset=True)
        if self.NUSTA >= 1:
            tmp, now_pos = self._read_record(now_pos, 'S', convert_type=_CalmetXYUpperStations1, add_to_dataset=True)
            tmp, now_pos = self._read_record(now_pos, 'S', convert_type=_CalmetXYUpperStations2, add_to_dataset=True)
        if self.NPSTA >= 1:
            tmp, now_pos = self._read_record(now_pos, 'S', convert_type=_CalmetXYPrecStations1, add_to_dataset=True)
            tmp, now_pos = self._read_record(now_pos, 'S', convert_type=_CalmetXYPrecStations2, add_to_dataset=True)

        tmp, now_pos = self._read_record(now_pos, 'S', convert_type=_CalmetSurfRough, add_to_dataset=True)
        tmp, now_pos = self._read_record(now_pos, 'S', convert_type=_CalmetLanduse, add_to_dataset=True)
        tmp, now_pos = self._read_record(now_pos, 'S', convert_type=_CalmetElev, add_to_dataset=True)
        tmp, now_pos = self._read_record(now_pos, 'S', convert_type=_CalmetLeafAreaIndex, add_to_dataset=True)

        if self.NSSTA >= 1:
            tmp, now_pos = self._read_record(now_pos, 'S', convert_type=_CalmetNearestSurfStationNo, add_to_dataset=True)


    def _read_record(self, pos, dtype, shape=1, convert_type=None, add_to_dataset=False):
        recsize = np.memmap(self._f, dtype='i4', mode='c', offset=pos, shape=(1,))[0]
        if convert_type is None:
            if dtype == 'S':
                dtype = 'S%d' % recsize
            data = np.memmap(self._f, dtype=dtype, mode='c', offset=pos+4, shape=shape)
            if shape == 1:
                data = data[0]
        else:
            c = 0
            new_cv_type = []
            for cp in convert_type:
                name = cp[0]
                tp = cp[1]
                if name == 'IDUM':
                    name = 'IDUM%d' % c
                    c += 1
                if '%' in tp:
                    tp = tp % self.__dict__
                new_cv_type.append( (name, tp) )
            self._f.seek(pos+4)
            data = np.fromfile(self._f, dtype=new_cv_type, count=1)[0]
            if add_to_dataset is True:
                for i, cp in enumerate(new_cv_type):
                    if not cp[0].startswith('IDUM'):
                        self.__dict__[cp[0]] = data[i]

        return data, pos + recsize + 8




