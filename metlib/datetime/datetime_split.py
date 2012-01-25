#!/usr/bin/env python

import numpy as np
import sys
from logical import *

def datetime_split(rec, dts=None, funcs=[]):
    if dts is None:
        dts = rec['datetime']
    bins = []
    for func in funcs:
        part = rec[np.where(func(dts))]
        bins.append(part)
    return bins

def split_season(rec, dts=None):
    return datetime_split(rec, dts, funcs=[
        lambda s: season_is('spring', s),
        lambda s: season_is('summer', s),
        lambda s: season_is('autumn', s),
        lambda s: season_is('winter', s)
        ]
        )

def split_month(rec, dts=None):
    return datetime_split(rec, dts, 
            funcs=[lambda s, month=month: month_is(month, s) for month in range(1, 13)])

def split_weekday(rec, dts=None):
    return datetime_split(rec, dts, 
            funcs=[lambda s, weekday=weekday: weekday_is(weekday, s) for weekday in range(1, 8)] )

def split_hour(rec, dts=None):
    return datetime_split(rec, dts, 
            funcs=[lambda s, hour=hour: hour_is(hour, s) for hour in range(0,24)] )

def split_year(rec, dts=None, start_year=None, end_year=None):
    if dts is None:
        dts = rec['datetime']
    if start_year is None:
        start_year = dts[0].year
    if end_year is None:
        end_year = dts[-1].year + 1
    return datetime_split(rec, dts, 
            funcs=[lambda s, year=year: year_is(year, s) for year in range(start_year, end_year)] )
