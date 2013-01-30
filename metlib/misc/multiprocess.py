#!/usr/bin/env python

# multiprocess.py

import os
import re
#from datetime import datetime, timedelta
#from dateutil.parser import parse
import numpy as np
from multiprocessing import Process
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#from matplotlib import mlab
#from netCDF4 import Dataset

__all__ = ['JobSplitter', 'split_job']

class JobSplitter(object):
    """
    """
    def __init__(self, func, arg_list, cpu_number=1):
        """
        """
        self.func = func
        self.arg_list = arg_list
        self.cpu_number = cpu_number
        self.jobs = []

    def run(self, wait=True):
        self.jobs = []
        each_job_load = int(np.ceil(len(self.arg_list) / float(self.cpu_number)))
        for i in range(self.cpu_number):
            p = Process(target=self.func, args=(self.arg_list[i*each_job_load:(i+1)*each_job_load], ))
            self.jobs.append(p)
        for job in self.jobs:
            job.start()
        if wait:
            for job in self.jobs:
                job.join()

def split_job(func, arg_list, cpu_number=1, wait=True):
    """split_job splits jobs to multi-processes.

Parameters
----------
func: the func which accepts one sequence as its only arg.
arg_list: the list of arg for func, which will be splitted according to cpu_number.
cpu_number: number of processes.
wait: whether wait until all jobs are done.
"""
    the_jobs = JobSplitter(func, arg_list, cpu_number=cpu_number)
    the_jobs.run(wait=wait)

if __name__ == '__main__':
    import time
    def myfunc(arg):
        print arg
        for i in xrange(10000000):
            ii = i*i

#    Jobs = JobSplitter(myfunc, range(100), 10)
#    Jobs.run()
    split_job(myfunc, range(100), 4, wait=True)
    print "Done"
    
