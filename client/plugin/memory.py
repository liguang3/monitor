#!/usr/bin/env python
# encoding: utf-8
"""@version: ??
@author: Daven Li
@file: cpu.py
@time: 2017/8/15 8:09
"""
import time
def monitor():
    with open('/proc/meminfo') as f:
        MemTotal = float(f.readline().split()[1])
        MemFree = float(f.readline().split()[1])
	MemAvailable= float(f.readline().split()[1])
        Buffers = float(f.readline().split()[1])
        Cached = float(f.readline().split()[1])
	value_dic = {}
	value_dic={
            'MemTotal':MemTotal,
            'MemFree':MemFree,
            'MemAvailable':MemAvailable,
           'Buffers':Buffers,
            'Cached':Cached,
	   'status':"0"
        }
	return value_dic

if __name__ == '__main__':
    print monitor()
