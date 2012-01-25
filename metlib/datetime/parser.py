#!/usr/bin/env python

import re
from datetime import datetime, timedelta
from dateutil.parser import parse
import numpy as np

__all__ = ['parse_datetime', 'parse_timedelta']

def parse_datetime(timestr):
    """Try parse timestr or integer or list of str/integer into datetimes"""
    return_single = False
    if isinstance(timestr, (int, long, np.integer, str, unicode)):
        timestrs = [timestr]
        return_single = True
    else:
        timestrs = timestr
    res_list = []
    for timestr in timestrs:
        if isinstance(timestr, (int, long, np.integer)):
            timestr = str(timestr)
        if len(timestr) == 10:
            timestr = timestr + '00'
        try:
            res = parse(timestr)
        except ValueError:
            res = None
        res_list.append(res)
    if return_single:
        return res_list[0]
    else:
        return res_list

_tdelta_dict = {'d':'days', 'h':'hours', 'm':'minutes', 's':'seconds'}
def parse_timedelta(timestr):
    """Try parse timestr or integer or list of them into timedeltas.
    e.g. parse_timedelta(['30m', '2h', '1d', '15s']).
    d: days
    h: hours
    m: minutes
    s: seconds (default)
    """
    return_single = False
    if isinstance(timestr, (int, long, np.integer, str, unicode)):
        timestrs = [timestr]
        return_single = True
    else:
        timestrs = timestr
    res_list = []
    for timestr in timestrs:
        if isinstance(timestr, (int, long, np.integer)):
            timestr = str(timestr)
        timestr = timestr.lower().strip()
        m = re.match(r'([-0-9]+)([dhms]*)', timestr)
        if not m:
            res = None
        else:
            value = int(m.group(1))
            symbol = m.group(2)
            if symbol == '':
                symbol = 's'
            res = timedelta(**{_tdelta_dict[symbol]:value})
        res_list.append(res)
    if return_single:
        return res_list[0]
    else:
        return res_list

if __name__ == '__main__':
    print parse_datetime(20090101)
    print parse_datetime([20110101, 2011010201, 20110103010101])
    print parse_datetime(['20110101', '2011010201', '20110103010101'])
    print parse_timedelta('35d')
    print parse_timedelta([35, 40, 2, -3])
    print parse_timedelta(['35', '40m', '2d', '-3h'])
