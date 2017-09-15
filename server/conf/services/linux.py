#!/usr/bin/env python
#coding:utf-8
from  generic import BaseService
from data_process import avg,hit,last
class CPU(BaseService):
        def __init__(self):
            super(CPU,self).__init__()
            self.name = 'linux_cpu'#全局唯一
            self.interval = 30 #监控间隔
            self.plugin_name = 'get_cpu_status'#让客户端知道该调用哪个插件
            self.triggers = {
                'idle':{
                    'func':'avg',
                    'last':10*60,
                    'count':5,
                    'operator':'lt', #使用什么公式处理<  idle越大越好
                    'warning':95,
                    'critical':80,
                    'data_type': float #增加扩展性
                },
                'iowait':{#从硬盘或内存读数据，系统iowait一直高表示硬盘慢，或程序大量io阻塞cpu，超过30%就比较忙的了，超过50就有问题了。
                    'func':'hit',
                    'minutes':15*60, #最近15分钟
                    'count':5,
                    'operator':'gt',
                    'threshod':'3',
                    'warning':10,
                    'critical':20,
                    'data_type':float
                },
                }
class Memory(BaseService):
        def __init__(self):
            super(Memory,self).__init__()
            self.name = 'linux_mem'#全局唯一
            self.interval = 30 #监控间隔
            self.plugin_name = 'get_mem_status'#让客户端知道该调用哪个插件
            self.triggers = {
               # 'MemUsage':{
                'MemAvailable':{
                    'func':'avg',
                    'minutes':5*60,
                    'count':1,
                    'operator':'lt',
                    'warning':260000,
                    'critical':150000,
                    'data_type':float
                },
                }
class Network(BaseService):
    def __init__(self):
        super(Network,self).__init__()
        self.interval = 60
        self.name = 'linux_network'
        self.plugin_name= 'get_net_status'
        self.triggers={
            'in':{
                'func':'hit',
                'last':10*60,
                'count':5,
                'operator':'gt',
                'warning':1024*1024*10, #10兆流量
                'critical':1024*1024*15,  #15
                'data_type': float
            },
            'out':{
                 'func':'hit',
                'last':10*60,
                'count':5,
                'operator':'gt',
                'warning':1024*1024*10, #10兆流量
                'critical':1024*1024*15,  #15
                'data_type': float
            }
        }















