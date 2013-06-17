#!/usr/bin/env python
import os
from glob import glob
import re
import shutil

__all__ = ['filesize', 'force_rm', 'force_makedirs', 'expand_path', 'get_rel_path', 'find_link_orig']

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
    # TODO, add regex support. and make it more robust.
    fnames = glob(fname)
    for fn in fnames:
        try:
            if os.path.islink(fn):
                os.unlink(fn)
            elif os.path.isdir(fn):
                shutil.rmtree(fn)
            else:
                os.remove(fn)
        except Exception as e:
            print e

def force_makedirs(dirname, rm_exist_dir=False):
    """force to make dir, no matter whether it exists"""
    #TODO: make it more robust
    if dirname in ['', '.', '..', './', '../', '/']:
        return
    orig = dirname
    if os.path.islink(orig):
        orig = find_link_orig(dirname)
    if os.path.isfile(orig):
        if not rm_exist_dir:
            raise RuntimeError('Cannot makedirs: %s is file' % dirname)
    if rm_exist_dir:
        try:
            force_rm(dirname)
        except Exception as e:
            pass
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != 17:
            raise e

def expand_path(path):
    """expandvars, expanduser"""
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    return path

def get_rel_path(path, base):
    """get relative path, e.g., get_rel_path('abc/de/fg', 'abc') => 'de/fg'
    """
    lb = len(base)
    assert path[:lb] == base
    if path[lb] == '/':
        rel_path = path[lb+1:]
    else:
        rel_path = path[lb:]
    return rel_path

def find_link_orig(path, max_depth=99):
    """Try to find the orig of a link."""
    count = 0
    while count < max_depth:
        if os.path.islink(path):
            path = os.readlink(path)
        else:
            return path
        count += 1
    return path

