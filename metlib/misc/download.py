#!/usr/bin/env python

# download.py

import os
import requests
import time
from datetime import datetime
from dateutil import tz
from dateutil.parser import parse
from metlib.shell.fileutil import *


__all__ = ['Downloader', 'download']

class Downloader(object):
    def __init__(self, url, dest, info_timeout=30, download_timeout=None, **kwargs):
        self.url = url
        self.dest = dest
        self.info_timeout = info_timeout
        self.download_timeout = download_timeout
        self.request_kwargs = kwargs
        self.r = None
        self.remote_size = 0
        self.local_size = 0
        self.remote_modify_time = parse('19010101000000 UTC')
        self.local_modify_time = parse('19000101000000 UTC')

    def get_remote_info(self):
        self.r = requests.get(self.url, stream=True, timeout=self.info_timeout, **self.request_kwargs)
        if self.r.status_code != 200:
            return False
        self.remote_modify_time = parse(self.r.headers['last-modified'])
        self.remote_size = int(self.r.headers['content-length'])
        return True

    def get_local_info(self):
        if not os.path.exists(self.dest):
            return False
        self.local_size = filesize(self.dest)
        self.local_modify_time = datetime.fromtimestamp(os.path.getmtime(self.dest), tz.tzlocal())
        return True

    def whether_download(self):
        self.get_remote_info()
        self.get_local_info()
        if self.local_modify_time > self.remote_modify_time:
            return 'up to date'
        elif self.local_modify_time < self.remote_modify_time:
            return 'need download'
        else:
            if self.local_size == self.remote_size:
                return 'up to date'
            elif self.local_size < self.remote_size:
                return 'need append'
            else:
                return 'overflow'
        
    def download(self, retry=3, interval=60, append=True):
        outdir = os.path.dirname(self.dest)
        force_makedirs(outdir)
        retry_count = 0
        while retry_count < retry:
            try:
                wd = self.whether_download()
                if wd in ['up to date']:
                    return True
                elif wd in ['need download', 'overflow']:
                    force_rm(self.dest)
                    self.retrieve_file()
                elif wd in ['need append']:
                    if not append:
                        force_rm(self.dest)
                    self.retrieve_file()

            except Exception as e:
                print e
                time.sleep(interval)
            finally: 
                retry_count += 1
        wd = self.whether_download()
        if wd in ['up to date']:
            return True
        else:
            return False

    
    def retrieve_file(self):
        outf = open(self.dest, 'a')
        begpos = self.local_size
        if begpos != 0:
            resp = requests.get(self.url, stream=True, timeout=self.info_timeout, headers = {'Range':'bytes=%d-%d' %(begpos, self.remote_size-1)}, **self.request_kwargs)
        else:
            resp = self.r
        try:
            for data in resp.iter_content(chunk_size=1024):
                outf.write(data)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            pass
        finally:
            outf.close()
            self.change_dest_time()
            self.get_local_info()
 
    def change_dest_time(self):
        rmt_as_local = self.remote_modify_time.astimezone(tz.tzlocal())
        tstamp = time.mktime(rmt_as_local.timetuple())
        os.utime(self.dest, (tstamp, tstamp))

def download(url, dest, retry=3, interval=60, append=True, **kwargs):
    dler = Downloader(url, dest, info_timeout=60, **kwargs)
    res = dler.download(retry=retry, interval=interval, append=append)
    return res
    
if __name__ == '__main__':
    pass
