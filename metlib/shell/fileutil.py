#!/usr/bin/env python
import os

__all__ = ['filesize']

def filesize(fname):
    return os.stat(fname).st_size
