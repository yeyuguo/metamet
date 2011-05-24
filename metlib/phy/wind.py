import numpy as np

def wswd2uv(ws, wd):
    """Convert wind speed and wind direction to u, v.
    ws: wind speed
    wd: wind direction (in degrees, north wind is 0, east wind is 90, etc)
    Returns: u, v
    """
    wd = np.deg2rad(np.array(wd))
    ws = np.array(ws)
    u = -ws * np.sin(wd)
    v = -ws * np.cos(wd)
    return u, v

def uv2wswd(u, v):
    """Convert u, v wind to wind speed and wind direction.
    u , v : u, v wind.
    Returns: ws, wd
    ws: wind speed
    wd: wind direction (in degrees, north wind is 0, east wind is 90, etc)
    """
    u = np.array(u)
    v = np.array(v)
    ws = np.sqrt(u ** 2 + v ** 2)
    wd = np.fmod(np.rad2deg(np.arctan2(u, v)) + 180.0 , 360.0)
    return ws, wd

