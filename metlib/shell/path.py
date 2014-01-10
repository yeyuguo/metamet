import os
import re
from metlib.shell.fileutil import P

__all__ = ['sorted_walk', 'list_all_file', 'LS', 'CD']

def sorted_walk(top, **kwarg):
    """returns the sorted result in a list consisting os.walk's 3-tuple: (dirpath, dirnames, filename). 
    kwargs: os.path's kwargs, i.e. topdown=True[, onerror=None[, followlinks=False]]"""
    if 'followlinks' not in kwarg:
        kwarg['followlinks'] = True
    w = os.walk(top, **kwarg)
    res = list(w)
    res.sort()
    for stuff in res:
        stuff[1].sort()
        stuff[2].sort()
    return res

def list_all_file(top='.', fname_pattern=r'.*', dir_pattern=r'.*', ignore_hidden=True, **kwarg):
    """returns a list of filenames that matches the 2 regex patterns, 
    kwargs: os.path's kwargs, i.e. topdown=True[, onerror=None[, followlinks=False]]"""
    try:
        newtop = os.path.expanduser(os.path.expandvars(top))
    except:
        newtop = top
    if 'followlinks' not in kwarg:
        kwarg['followlinks'] = True
    walktuplelist = sorted_walk(newtop, **kwarg)
    filelist = []
    for walktuple in walktuplelist:
        d = walktuple[0]
        if re.search(dir_pattern, d):
            if ignore_hidden:
                sorted_dirs = sorted(d.split(os.path.sep))
                sorted_dirs = [subd for subd in sorted_dirs if subd not in ('', '.', '..')]
                if len(sorted_dirs) > 0 and sorted_dirs[0].startswith('.'):
                    continue
            for fname in walktuple[2]:
                if re.search(fname_pattern, fname):
                    if ignore_hidden:
                        if fname.startswith('.') or fname.endswith('~'):
                            continue
                    filelist.append(os.path.join(d, fname))
    return filelist

LS = list_all_file
def CD(path=None):
    if path is None:
        path = P('~')
    else:
        path = P(path)
    return os.chdir(path)
