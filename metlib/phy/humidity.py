#!/usr/bin/env python

import numpy as np
from .constants import *

def hum_r2q(r):
    "Humidity conversion r(mix ratio) to q(specific humidity)"
    return r / (1.0 + r)

def hum_q2r(q): #TODO
    "Humidity conversion q to r(mix ratio)"
    pass

def hum_e2r(e, p=p_std):
    "Humidity conversion e(vapor pressure) to r(mix ratio). Pressure Unit: hPa."
    return epsilon_vapor * e / (p - e)

def hum_e2q(e, p=p_std):
    "Humidity conversion e(vapor pressure) to q(specific humidity). Pressure Unit: hPa."
    return epsilon_vapor * e / (p - 0.378 * e)
#TODO hum_r2e 
def hum_q2e(q, p=p_std):
    "Humidity conversion q(specific humidity) to e(vapor pressure). Pressure Unit: hPa."
    return p * q / (epsilon_vapor + 0.378 * q)

def hum_e2rho_v(e, T=T_std):
    "Humidity conversion e(vapor pressure) to rho_v(vapor density)"
    T = auto2K(T)
    return epsilon_vapor * e / (R_d * T)

def hum_es(T):
    "Compute e_satuation for water surface"
    T = auto2K(T)
    return 6.1078 * np.exp(17.2693882*(T-273.16)/(T-35.86))

def hum_esi(T):
    "Compute e_satuation for ice surface"
    T = auto2K(T)
    return 6.1078 * np.exp(21.8745584*(T-273.16)/(T-7.66))

def hum_rh2e(rh, T, water_surface=True):
    "Humidity conversion RH to e (vapor pressure)"
    if water_surface:
        return (rh / 100.0) * hum_es(T)
    else:
        return (rh / 100.0) * hum_esi(T)

def hum_rh2q(rh, T, p=p_std, water_surface=True):
    "Humidity conversion RH to q (specific humidity)"
    return hum_e2q(hum_rh2e(rh, T, water_surface), p)

