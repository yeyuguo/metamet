import os
import re

__all__ = ['sorted_walk', 'list_all_file']

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

def list_all_file(top='.', fname_pattern=r'.*', dir_pattern=r'.*', **kwarg):
    """returns a list of filenames that matches the 2 regex patterns, 
    kwargs: os.path's kwargs, i.e. topdown=True[, onerror=None[, followlinks=False]]"""
    try:
        newtop = os.path.expanduser(os.path.expandvars(top))
    except:
        newtop = top
    walktuplelist = sorted_walk(newtop, **kwarg)
    filelist = []
    for walktuple in walktuplelist:
        d = walktuple[0]
        if re.search(dir_pattern, d):
            for fname in walktuple[2]:
                 if re.search(fname_pattern, fname):
                    filelist.append(os.path.join(d, fname))
    return filelist
