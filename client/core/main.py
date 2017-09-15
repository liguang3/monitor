#!/usr/bin/env python
#coding:utf-8
import os,sys
base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_dir)
import redishelper
import global_setting
from conf import settings
import json
import time
import threading
from plugin import cpu,plugin_api

class MonitorClient(object):
    def __init__(self):
        self.r=redishelper.RedisHelper()
        self.ip = settings.ClientIP
        self.host_config = self.get_host_config()
    def start(self):
        self.handle()
    def get_host_config(self):
        config_key = "HostConfig::%s" %self.ip
        config = self.r.get(config_key)
        if config:
            config = json.loads(config)
        return config
    def handle(self):
        if self.host_config:
            while True:
                for service,val in self.host_config.items(): #{'linux_network': ['get_net_status', 60], 'linux_cpu': ['get_cpu_status', 30]}
                    if len(val)<3:#确保第一次客户端启动时会运行所有插件
                        self.host_config[service].append(0)  #增加一列上次运行时间
                    plugin_name,interval,last_run_time = val  #插件名，间隔，时间戳
                    if time.time()-last_run_time<interval:#not reached the next run yet
                        next_run_time = interval-(time.time()-last_run_time)
                        print 'Service %s next run time is in [%s] secs' %(service,next_run_time)
                    else:
                        print "--going to run the [%s] again" %service
                        self.host_config[service][2] = time.time()
                        t= threading.Thread(target=self.call_plugin,args=(service,plugin_name))
                        t.start()

                time.sleep(10)

        else:
            print "\033[31;1mCannot get host config\033[0m"
    def call_plugin(self,service_name,plugin_name):
        func = getattr(plugin_api,plugin_name)
        service_data=func()
        report_data = {
        'host':self.ip,
        'service':service_name,
        'data':service_data
    }
        self.r.public(json.dumps(report_data))
        print 'service[%s] res:%s' %(service_name,service_data)



