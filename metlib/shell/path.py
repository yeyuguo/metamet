import os

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

