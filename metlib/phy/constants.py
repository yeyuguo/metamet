from scipy.constants import *

# NOTICE: R_star from US Atmos 1976 is a strange stuff
R_star = 8.31432E3  # J / ((k mol) * K)

M_d = 28.9644    # g / mol
M_v = 18.0159    # g / mol
R_d = 287.05        # J / (kg * K)
c_pd = 1004.0       # J / (kg * K)
c_vd = 717.0        # J / (kg * K)

epsilon_vapor = 0.622
p_std = 101325.0    # Pa
T_std = 273.15      # K
T_room = 298.0      # K

# # units['unit'] is the ratio to a standard unit:
# # for length: meter
# # for time : second
# # for weight : g
# # for concentration : 1.0

units = {
    'one': 1.0,
    'unit': 1.0,
    'k': 1E3,
    'M': 1E6,
    'G': 1E9,
    'T': 1E12,
    'm' : 1.0,
    'cm' : 1E-2,
    'mm' : 1E-3,
    'um' : 1E-6,
    'mum' : 1E-6,
    'nm' : 1E-9,
    'A'  : 1E-10,
    'g' : 1.0,
    'kg': 1E3,
    'ton': 1E6,
    'short ton':short_ton * 1E3,
    'minute': 60.0,
    'second': 1.0,
    'hour': 3600.0,
    'day': 86400.0,
    'ppm': 1E-6,
    'ppb': 1E-9,
    'ppt': 1E-12,
}
