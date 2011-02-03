from netCDF4 import Dataset
from pyproj import Proj
import numpy as np

class M3_Data_Pos(object):
    def __init__(self):
        self.i = 0
        self.j = 0
        self.k = 0
        self._points = None
        self._weights = None


class M3_File(object):
    """M3_File contains several useful attrs and functions.
    attrs:
        f: a netCDF4.Dataset object which contains everything in the M3 file
        proj: a pyproj.Proj object for coordinate conversion
    """

    def __init__(self, fname, mode='r'):
#        print "Opening file %s" % fname
        self.f = Dataset(fname, mode=mode)
#        print "Done"

#        print "Initing map"
        self.proj = Proj(
                proj='lcc',
                lat_0 = self.f.YCENT,
                lon_0 = self.f.XCENT,
                lat_1 = self.f.P_ALP, 
                lat_2 = self.f.P_BET,
                a=6370000.,
                b=6370000.
                )
#        print "Done"

    def lonlat_to_xy(self, lon, lat):
        return self.proj(lon,lat)

    def lonlat_to_ij(self, lon, lat, dot=False):
        x, y = self.lonlat_to_xy(lon, lat)
        i = (x - self.f.XORIG) / self.f.XCELL
        j = (y - self.f.YORIG) / self.f.YCELL
        if not dot:
            i -= 0.5
            j -= 0.5
        return i, j
    
    def xy_to_lonlat(self, x, y):
        return self.proj(x, y, inverse=True)

    def ij_to_xy(self, i, j, dot=False):
        if not dot:
            i = i + 0.5
            j = j + 0.5
        x = i * self.f.XCELL + self.f.XORIG
        y = j * self.f.YCELL + self.f.YORIG
        return x, y

    def ij_to_lonlat(self, i, j, dot=False):
        x, y = self.ij_to_xy(i, j, dot=dot)
        return self.xy_to_lonlat(x, y)

#    def get_data_pos(self, lon, lat, height, dot=False):
#        i, j = self.lonlat_to_ij(lon, lat, dot=dot)
#        if i < -0.5 or j < -0.5 \
#                or i > self.f.NCOLS - 0.5 \
#                or j > self.f.NROWS - 0.5:
#            return None
#        elif i < 0.5 or j < 0.5 \
#                or i > self.f.NCOLS - 1.5 \
#                or j > self.f.NROWS - 1.5:
#            pass       
#
#    def get_data(self, varname, data_pos):
#        pass

    def get_time_serie(self, varname, lon, lat, level=0, dot=False):
        i, j = self.lonlat_to_ij(lon, lat, dot=dot)
        i = int(round(i))
        j = int(round(j))
        return self.f.variables[varname][:,level, j, i]
    
    def get_xy_arrays(self, dot=False):
        i = np.arange(len(self.f.dimensions['COL']), dtype=int)
        j = np.arange(len(self.f.dimensions['ROW']), dtype=int)
        ii, jj = np.meshgrid(i, j)
        x, y = self.ij_to_xy(ii, jj, dot=dot)
        return x, y
    
    def get_lonlat_arrays(self, dot=False):
        x, y = self.get_xy_arrays(dot=dot)
        lon, lat = self.xy_to_lonlat(x, y)
        return lon, lat
    
