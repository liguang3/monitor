#!/usr/bin/env python
# encoding: utf-8
"""@version: ??
@author: Daven Li
@file: plugin_api.py
@time: 2017/8/15 8:08
"""
import load,cpu,memory
def get_network_status():
    return load.monitor()

def get_cpu_status():
    return cpu.monitor()

def get_mem_status():
    return memory.monitor()