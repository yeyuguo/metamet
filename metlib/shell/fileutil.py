#!/usr/bin/env python
import os

__all__ = ['filesize']

def filesize(f):
    """Return the size of f in bytes"""
    if isinstance(f, file):
        now_pos = f.tell()
        f.seek(0, 2)
        size = f.tell()
        f.seek(now_pos)
        return size
    else:
        return os.stat(f).st_size

def force_rm(fname, regex=False):
    """force to rm fname, no matter whether fname is file, dir or link"""
    # TODO, and when completed, add to __all__
    # TODO, add glob support and regex support.
    pass

def force_makedirs(dirname, rm_exsit_dir=False):
    """force to make dir, no matter whether it exists"""
    # TODO, and when completed, add to __all__
    pass

def expand_path(path):
    """expandvars, expanduser"""
    # TODO
    pass
