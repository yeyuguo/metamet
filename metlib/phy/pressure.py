#!/usr/bin/env python

import numpy as np
from .constants import *

def dz_dp(p, Tv):
    "-dz/dp. p:hPa, Tv: deg C, result: m/hPa"
    return Rd*(Tv+273.15)/(p*9.80665)

