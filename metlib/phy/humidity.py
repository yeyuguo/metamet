#!/usr/bin/env python

import numpy as np
from .constants import *

def hum_r2q(r):
    "Humidity conversion r(mix ratio) to q(bi shi)"
    return r / (1.0 + r)

def hum_q2r(q): #TODO
    "Humidity conversion q to r(mix ratio)"
    pass

def hum_e2r(e, p=p_std):
    "Humidity conversion e(vapor pressure) to r(mix ratio)"
    return epsilon_vapor * e / (p - e)

def hum_e2q(e, p=p_std):
    "Humidity conversion e(vapor pressure) to q(bi shi)"
    return epsilon_vapor * e / (p - 0.378 * e)
#TODO hum_r2e, hum_q2e

def hum_e2rho_v(e, T=T_std):
    "Humidity conversion e(vapor pressure) to rho_v(vapor density)"
    return epsilon_vapor * e / (R_d * T)

def hum_es(T):
    "Compute e_satuation for water surface"
    if T < 100.0:
        T = T + 273.15
    return 6.1078 * np.exp(17.2693882*(T-273.16)/(T-35.86))

def hum_esi(T):
    "Compute e_satuation for ice surface"
    if T < 50.0:
        T = T + 273.15
    return 6.1078 * np.exp(21.8745584*(T-273.16)/(T-7.66))
