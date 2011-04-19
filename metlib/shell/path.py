import os
import re

def sorted_walk(top, **kwarg):
    """returns the sorted result in a list consisting os.walk's 3-tuple: (dirpath, dirnames, filename). 
    kwargs: os.path's kwargs, i.e. topdown=True[, onerror=None[, followlinks=False]]"""
    w = os.walk(top, **kwarg)
    res = list(w)
    res.sort()
    for stuff in res:
        stuff[1].sort()
        stuff[2].sort()
    return res

def list_all_file(top, dir_pattern=r'.*', fname_pattern=r'.*', **kwarg):
    """returns every filename that matches the 2 patterns in a flat list, 
    kwargs: os.path's kwargs, i.e. topdown=True[, onerror=None[, followlinks=False]]"""
    walktuplelist = sorted_walk(top, **kwarg)
    filelist = []
    for walktuple in walktuplelist:
        d = walktuple[0]
        if re.search(dir_pattern, d):
            for fname in walktuple[2]:
                 if re.search(fname_pattern, fname):
                    filelist.append(os.path.join(d, fname))
    return filelist
