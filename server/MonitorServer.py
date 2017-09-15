#!/usr/bin/env python
#coding:utf-8
from core import main
from conf  import settings
import os,sys
'''
base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_dir)
print base_dir
print sys.path
'''
import sys
import os
sys.path.append('C:\\Users\\liguang\\Desktop\\pytest\\febushi\\server')
if __name__ == '__main__':
    server = main.MonitorServer()
    server.save_configs()
    server.start()