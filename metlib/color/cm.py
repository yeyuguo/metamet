#!/usr/bin/env python

from matplotlib.colors import LinearSegmentedColormap as LSCM
from .color_collections import *

_bb = 'CornflowerBlue'
_br = 'DarkRed'
_cm_GateRdBu1_data = (
        (0.0, _br), (0.5, _br), (0.5, _bb), (1.0, _bb)
        )
_cm_GateRdBu2_data = (
        (0.0, _br), (0.95, _br), (0.95, _bb), (1.0, _bb)
        )
_cm_GateBuRd2_data = (
        (0.0, _bb), (0.95, _bb), (0.95, _br), (1.0, _br)
        )
_cm_GateBuRd_data = (
        (0.0, 'Navy'), (0.5, _bb), (0.5, _br), (1.0, 'OrangeRed')
        )
_cm_pop_poster_data = list(pop_poster)
_cm_crayon_data = crayon[:14]
_cm_crayon_dark_data = crayon_dark[:10]

_cm_night_data = [(0.0, '#27013a'), (0.1667, '#4763f7'), (0.3, '#82d6fa'), (0.45, '#92fee5'), (0.5, '#8ffe41'), (0.6667, '#efd743'), (0.85, '#cc2338'), (0.89, '#cd243e'), (0.94, '#e07ef0'), (0.985, '#f3d9f6'), (1.0, '#eedadc')]     
_cm_delight_data = ['#FFFFFF', '#874ac8', '#5419ad', '#2a36d6', '#0251fc', '#00e8ff', '#00f300', '#009000', '#5fc400', '#ffff00', '#ff7e00', '#ff0000', '#6d0000']            


todo_dict = {
        'cm_night':_cm_night_data,
        'cm_delight':_cm_delight_data,
        'cm_GateRdBu1':_cm_GateRdBu1_data,
        'cm_GateRdBu2':_cm_GateRdBu2_data,
        'cm_GateBuRd2':_cm_GateBuRd2_data,
        'cm_GateBuRd':_cm_GateBuRd_data,
        'cm_pop_poster':_cm_pop_poster_data,
        'cm_crayon':_cm_crayon_data,
        'cm_crayon_dark':_cm_crayon_dark_data,
        'cm_brewer_PuOr': brewer_PuOr,
        'cm_brewer_BrBG': brewer_BrBG,
        'cm_brewer_PRGn': brewer_PRGn,
        'cm_brewer_PiYG': brewer_PiYG,
        'cm_brewer_RdBu': brewer_RdBu,
        'cm_brewer_RdGy': brewer_RdGy,
        'cm_brewer_RdYlBu': brewer_RdYlBu,
        'cm_brewer_RdYlGn': brewer_RdYlGn,
        'cm_brewer_spectral': brewer_spectral,
        }

for _cm_name, _cm_data in todo_dict.items():
    if not _cm_name.endswith('_r') and _cm_name+'_r' not in todo_dict:
        if isinstance(_cm_data[0], tuple) and len(_cm_data[0]) == 2:
            # e.g. (0.0, (1.0, 0.0, 1.0))
            # or   (0.4, 'red')
            reversed_data = [(1.0-x, c) for x, c in reversed(_cm_data)]
        else:
            reversed_data = list(reversed(_cm_data))
    todo_dict[_cm_name + '_r'] = reversed_data

res_dict = dict()
for _cm_name, _cm_data in todo_dict.iteritems():
#    print _cm_name, _cm_data
    res_dict[_cm_name] = LSCM.from_list(_cm_name, _cm_data)

locals().update(res_dict)


__all__ = ['LSCM'] + [m for m in res_dict if m.startswith('cm_')]
