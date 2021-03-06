#!/usr/bin/env python
#coding:utf-8
import redishelper
import serialize
import global_setting
from conf import hosts
import json,time
import threading
class MonitorServer(object):
    def __init__(self):
        self.r = redishelper.RedisHelper()
        self.r.set('name','litest')
        self.save_configs()

    def start(self):
        self.data_handle()

        self.hand()

    def save_configs(self): #把所有的信息写到redis里面
        serialize.push_all_configs_into_redis(self,hosts.monitored_groups)

    def hand(self):
        chan_sub = self.r.subscribe()
        while True:
            host_service_data = chan_sub.parse_response()
            host_service_data = json.loads(host_service_data[2])
            host_service_data['time_stamp'] = time.time()  #服务器收到数据加上时间
            service_data_key = "ServiceData::%s::%s" %(host_service_data['host'],host_service_data['service'])
            self.r.set(service_data_key,json.dumps(host_service_data))

    def data_handle_run(self):
        serialize.data_process(self)

    def data_handle(self):
        t = threading.Thread(target=self.data_handle_run)
        t.start()
        '处理监控数据，独立线程'
    def alert_handle(self):
        '处理报警信息，独立线程'
        pass
