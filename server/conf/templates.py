#!/usr/bin/env python
#coding:utf-8
#coding:utf-8
#/usr/bin/env python
from services import linux
class BaseTemplate(object):
    def __init__(self):
        self.name = 'your template name'
        self.hosts = [] #把需要监控的放在这个模板里
        self.services = []
class LinuxGenericTemplate(BaseTemplate):
    def __init__(self):
        super(LinuxGenericTemplate,self).__init__()
        self.name ="LinuxCommonService"
        self.services = [
            linux.CPU(),#类名，类的内存对象
            linux.Memory()
        ]
        self.services[0].interval = 90

class Linux2(BaseTemplate):
    def __init__(self):
        super(Linux2,self).__init__()
        self.name = 'linux2'
        self.services =[
            linux.CPU(),
            linux.Network()
        ]