#!/usr/bin/env python

# misc.py

import os, sys
import re
import pickle
#from datetime import datetime, timedelta
#from dateutil.parser import parse
import numpy as np
import collections
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#from matplotlib import mlab
#from netCDF4 import Dataset
from metlib.misc.datatype import Null

__all__ = ['struni', 'grep', 'strip_ext', 'sub_ext', 'get_ext', 'savepickle', 'loadpickle', 'str2list', 'get_sys_argv', 'parse_bool']

def struni(obj):
    """ return str(obj) if possible, else return unicode(obj).
    """
    try:
        res = str(obj)
        return res
    except UnicodeEncodeError as e:
        res = unicode(obj)
        return res

def grep(pattern, seq, flags=0):
    """grep greps patterns from seqs.
Parameters:
    pattern: regex pattern str or compiled regex pattern or func. 
    seq: seq of str or any other stuffs, etc. If pattern is not func and seq[0] is not str/unicode, seq will be converted using str() first.
    flags: 'ILMSUX' or number of re.I|re.L|re.M|re.S|re.U|re.X .
        I: ignore case;
        L: locale dependent;
        M: multi-line;
        S: dot matches all;
        U: unicode dependent;
        X: verbose.
Returns:
    A filtered list.
    """
    if isinstance(flags, (str, unicode)):
        true_flags = 0
        flags = flags.upper()
        for letter in flags:
            if letter in 'ILMSUX':
                true_flags += re.__dict__[letter]
    else:
        true_flags = flags
    if isinstance(pattern, (str, unicode, type(re.compile(r'')) ) ):
        res = []
        seq = [struni(item) for item in seq]
        for item in seq:
            if re.search(pattern, item, true_flags):
                res.append(item)
    elif callable(pattern):
        res = filter(pattern, seq)

    return res

def strip_ext(path):
    """strips .ext from a path"""
    return os.path.splitext(path)[0]

def get_ext(path):
    """get .ext from a path"""
    return os.path.splitext(path)[1]

def sub_ext(orig, new_ext):
    """sub .ext with a new one"""
    if not new_ext.startswith('.'):
        new_ext = '.' + new_ext
    return strip_ext(orig) + new_ext

def str2list(s, pattern=',|;|:|#|\||\s+'):
    return re.split(pattern, s)

def get_sys_argv(argnames=[], optional_argnames=[], keyword_argnames=[], desc=''):
    """get_sys_argv parse sys.argv according to a list of argnames. 
    Parsed args goes directly into globals().
    If not succeed, print a usage prompt and exit.

Parameters
----------
argnames: a list of arg names or tuples of (arg name, convert function).
optional_argnames: like argnames, but optional. It's best to specify default values for these optional args before calling get_sys_argv(), as shown in the example; otherwise the default value will be Null.
keyword_argnames: optional keyword args (e.g., kw1=..., kw2=...). If not specified, *NO* variable will be generated. So it's best to specify non-optional keyword values before calling get_sys_argv(). 
desc: additional descriptions.

Return
------
a list of remaining args.
And two extra dicts will be generated: _sys_argv_args, _sys_argv_kwargs

Example
-------
>>> job = 'sinner'
>>> status = 'not redeemed yet'
>>> get_sys_args( ['name', ('age', int)], ['job', 'status'])

    """
    class ExceptionHelp(Exception):
        pass

    nonkw_argv = []
    kw_argv = []
    for a in sys.argv[1:]:
        if '=' in a:
            kw_argv.append(a)
        else:
            nonkw_argv.append(a)
    kwargconvd = dict(keyword_argnames)
    argdict = dict()
    kwargdict = dict()
    true_argnames = []
    argconvd = dict()
    n_must = len(argnames)
    for a in argnames + optional_argnames:
        if isinstance(a, (str, unicode)):
            true_argnames.append(str(a))
        elif isinstance(a, (tuple, list)) \
                and len(a) == 2 \
                and isinstance(a[0], (str, unicode)) \
                and callable(a[1]):
            true_argnames.append(str(a[0]))
            argconvd[a[0]] = a[1]
    try:
        if len(sys.argv) == 2 and sys.argv[1] == "--help":
            raise ExceptionHelp()
        for i, argname in enumerate(true_argnames):
            if i >= len(nonkw_argv) and i >= n_must:
                for argn in true_argnames[i:]:
                    if argn not in sys.modules['__main__'].__dict__:
                        sys.modules['__main__'].__dict__[argn] = Null
                break
            value = nonkw_argv[i]
            if argname in argconvd:
                value = argconvd[argname](value)
            argdict[argname] = value
        for argstr in kw_argv:
            argname, value = argstr.split('=', 1)
            if argname in kwargconvd:
                value = kwargconvd[argname](value)
            kwargdict[argname] = value
        sys.modules['__main__'].__dict__.update(argdict)
        sys.modules['__main__'].__dict__.update(kwargdict)
        sys.modules['__main__'].__dict__['_sys_argv_args'] = argdict
        sys.modules['__main__'].__dict__['_sys_argv_kwargs'] = kwargdict
    except Exception as e:
        print "Usage:"
        print "    %s" % sys.argv[0], 
        for argn in true_argnames[:n_must]:
            print argn,
        if len(optional_argnames) > 0:
            print '[',
            for argn in true_argnames[n_must:]:
                print argn,
            print ']',
        if len(kwargconvd) > 0:
            print '{',
            for kwargn in kwargconvd:
                print '%s=' % kwargn,
            print '}',
        print
        for argn in true_argnames:
            if argn in argconvd:
                print "        %s will be converted by %s" % (argn, argconvd[argn])
        for kwargn, convfunc in kwargconvd.iteritems():
            if convfunc not in (str, unicode):
                print "        %s will be converted by %s" % (kwargn, convfunc)
        print desc
        if not isinstance(e, ExceptionHelp):
            print "Error:"
            print "    %s:" % argname, e
        sys.exit(1)
    other_args = nonkw_argv[len(true_argnames):]

    return other_args

def savepickle(fname, obj):
    outf = open(fname, 'w')
    pickle.dump(obj, outf)
    outf.close()

def loadpickle(fname):
    infile = open(fname)
    obj = pickle.load(infile)
    infile.close()
    return obj

def parse_bool(s):
    def _tobool(ss):
        ss = ss.upper()
        if ss in ['FALSE', 'F', 'NO', 'N', '0', '']:
            return False
        elif ss in ['TRUE', 'T', 'YES', 'Y', '1']:
            return True
        else:
            return bool(ss)

    if isinstance(s, (str, unicode)):
        if s.upper() in ['TRUE', 'FALSE', 'T', 'F', 'YES', 'NO', 'Y', 'N', '1', '0', '']:
            return _tobool(s)
        elif set(s.upper()) <= set(['T', 'F', '0', '1', 'Y', 'N']):
            return np.array([_tobool(ss) for ss in s])
        else: 
            return bool(s)
    elif isinstance(s, (collections.Sequence, np.ndarray)):
        return np.array([_tobool(ss) for ss in s])
    else:
        return bool(s)

if __name__ == '__main__':
    l = ['abcde', 'asldkfj', 'sdjfowij', 'sdfoijw', '1243450', '1204023']
    print grep(re.compile('sd'), l)
    print grep(r"^\d*$", l)
    print grep(lambda s: s.startswith('a'), l)
    p = 'abc/def/gh.hi.sf'
    print strip_ext(p)
    print get_ext(p)
    print sub_ext(p, 'txt')
