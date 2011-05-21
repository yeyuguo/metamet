#!/usr/bin/env python

from datetime import datetime, timedelta
import numpy as np

_s_m = {1:(3,4,5),2:(6,7,8),3:(9,10,11),4:(12,1,2),
        'spring':(3,4,5), 'summer':(6,7,8),
        'autumn':(9,10,11), 'winter':(12,1,2),
        'fall':(9,10,11)}

def year_is(years, the_datetime):
    years = np.array(years)
    the_datetime = np.array(the_datetime)
    res = np.zeros(the_datetime.shape, dtype='O')
    for i in range(res.size):
        res.flat[i] = True if the_datetime.flat[i].year \
                in years else False
    return res

def month_is(months, the_datetime):
    months = np.array(months)
    the_datetime = np.array(the_datetime)
    res = np.zeros(the_datetime.shape, dtype='O')
    for i in range(res.size):
        res.flat[i] = True if the_datetime.flat[i].month \
                in months else False
    return res

def hour_is(hours, the_datetime):
    hours = np.array(hours)
    the_datetime = np.array(the_datetime)
    res = np.zeros(the_datetime.shape, dtype='O')
    for i in range(res.size):
        res.flat[i] = True if the_datetime.flat[i].hour \
                in hours else False
    return res

def weekday_is(weekdays, the_datetime):
    """Notice: Mon is 1, Sun is 7, as iso weekday"""
    weekdays = np.array(weekdays)
    the_datetime = np.array(the_datetime)
    res = np.zeros(the_datetime.shape, dtype='O')
    for i in range(res.size):
        res.flat[i] = True if \
            the_datetime.flat[i].isoweekday() \
            in weekdays else False
    return res

def season_is(seasons, the_datetime):
    seasons = np.array(seasons)
    the_datetime = np.array(the_datetime)
    res = np.zeros(the_datetime.shape, dtype='O')
    months = set()
    global _s_m
    for s in seasons.flat:
        try:
            s = s.lower()
        except:
            pass
        months.update(_s_m[s])
    for i in range(res.size):
        res.flat[i] = True if the_datetime.flat[i].month \
                in months else False
    return res

def year_season_is(years, seasons, the_datetime):
    years = np.array(years)
    seasons = np.array(seasons)
    the_datetime = np.array(the_datetime)
    res = np.zeros(the_datetime.shape, dtype='O')
    months = set()
    global _s_m
    for s in seasons.flat:
        try:
            s = s.lower()
        except:
            pass
        months.update(_s_m[s])
    for i in range(res.size):
        dt = the_datetime.flat[i]
        extra = 1 if dt.month in (1,2) else 0
        res.flat[i] = True if (dt.month in months and \
                dt.year - extra in years) else False
    return res

def datetime_is_between(datetime_beg, datetime_end, 
        the_datetime):
    """Returns True if dt_beg <= the_datetime < dt_end"""
    the_datetime = np.array(the_datetime)
    res = np.zeros(the_datetime.shape, dtype='O')
    for i in range(res.size):
        dt = the_datetime.flat[i]
        res.flat[i] = True if dt >= datetime_beg and \
                dt < datetime_end else False
    return res
