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

todo_dict = {
        'cm_GateRdBu1':_cm_GateRdBu1_data,
        'cm_GateRdBu2':_cm_GateRdBu2_data,
        'cm_GateBuRd2':_cm_GateBuRd2_data,
        'cm_GateBuRd':_cm_GateBuRd_data,
        'cm_pop_poster':_cm_pop_poster_data,
        'cm_crayon':_cm_crayon_data,
        'cm_crayon_dark':_cm_crayon_dark_data,
        }

for cm_name, cm_data in todo_dict.items():
    if not cm_name.endswith('_r') and cm_name+'_r' not in todo_dict:
        if isinstance(cm_data[0], tuple) and len(cm_data[0]) == 2:
            # e.g. (0.0, (1.0, 0.0, 1.0))
            # or   (0.4, 'red')
            reversed_data = [(1.0-x, c) for x, c in reversed(cm_data)]
        else:
            reversed_data = list(reversed(cm_data))
    todo_dict[cm_name + '_r'] = reversed_data

res_dict = dict()
for cm_name, cm_data in todo_dict.iteritems():
#    print cm_name, cm_data
    res_dict[cm_name] = LSCM.from_list(cm_name, cm_data)

locals().update(res_dict)


__all__ = ['LSCM'] + list(res_dict.keys())
