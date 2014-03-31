import numpy as np
import sys, os, re
from datetime import datetime, timedelta
from matplotlib import mlab

from metlib.datetime import *
from metlib.data._all import rec_combine, rec_from_seqs, Basket, loadbasket, savebasket
from metlib.data._all import Limiter, nearest_i
from metlib.io.rec2csv_neat import rec2csv_neat
from metlib.misc._all import ma_out, grep, strip_ext, sub_ext, get_ext
from metlib.misc._all import split_job, savepickle, loadpickle, struni, str2list, get_sys_argv
from metlib.misc._all import limited_int, Singleton, NullClass, Null
from metlib.misc._all import isinteger, isfloat, isseq
from metlib.misc._all import int_sign, second_derivate
from metlib.misc._all import parse_bool
from metlib.misc._all import Setter
from metlib.plot._all import axgrid, axstack, format_ticks
from metlib.phy.wind import wswd2uv, uv2wswd
from metlib.shell import force_makedirs, expand_path, get_rel_path, find_link_orig, filesize, force_rm, list_all_file, get_output, LS, MKDIR, CD, P, CP, MV, RM, DIRNAME, BASENAME
from metlib.color.color_collections import *
import metlib.color.cm as metlib_cm

from matplotlib.pyplot import plot