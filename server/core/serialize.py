#!/usr/bin/env python
#coding:utf-8
import pickle
from conf import  hosts
import redishelper
import json
import time
import operator
from put_data_into_mysql.into_mysql import  *

def push_all_configs_into_redis(main_ins,host_groups):
    host_config_dic = {}
    for group in host_groups:
        for h in group.hosts:
            if h not in host_config_dic:
                host_config_dic[h]={}
            for s in group.services:
                host_config_dic[h][s.name]=[s.plugin_name,s.interval]
    for h,v in host_config_dic.items():
        host_config_key = "HostConfig::%s" %h
       # print host_config_key,json.dumps(v)
        main_ins.r.set(host_config_key,json.dumps(v))

def fetch_all_configs_into_redis(host_groups):
    host_config_dic = {}
    for group in host_groups:
        for h in group.hosts:
            if h not in host_config_dic:
                host_config_dic[h]={}
            for s in group.services:
                host_config_dic[h][s.name]=s
    #for h,v in host_config_dic.items():
      #print h,v
    return host_config_dic


def data_process(main_ins):

    print '--going to handle monitor data---'
    all_host_configs =fetch_all_configs_into_redis(hosts.monitored_groups)
    while True:
        for ip,service_dict in all_host_configs.items():
            for service_name,s_instance in service_dict.items():
                service_redis_key = "ServiceData::%s::%s" %(ip,service_name)
                s_data = main_ins.r.get(service_redis_key)


                if s_data:#error了
                    s_data = json.loads(s_data)
                    time_stamp = s_data['time_stamp']
                    if time.time() - time_stamp < s_instance.interval:

                        if str(s_data['data']['status'])=='0':#data valid

                            if service_name == 'linux_mem':
                                data_mem = Mem(totle= s_data['data']['MemTotal'],used=s_data['data']['MemAvailable'],ip=ip)
                                Session.add(data_mem)
                                Session.commit()
                            else:

                                data_cpu = Cpu(idle=s_data['data']['idle'],iowait=s_data['data']['iowait'],ip=ip)
                                Session.add(data_cpu)
                                Session.commit()



                            print 'add information successfully'




                            print "\033[32;1mHost[%s] Service[%s] data valid\033[0m" %(ip,service_name)
                            for item_key,val_dict in s_instance.triggers.items():#监控指标，阈值
                                service_item_handle(main_ins,item_key,val_dict,s_data,ip) #处理监控数据
                        else:
                            print   '\033[31;1mHost[%s] Service[%s] plugin error' %(ip,service_name)

                    else:#data expired
                        expired_time = time.time() - time_stamp-s_instance.interval
                        print '\033[31;1mHost[%s] Service[%s] data expred[%s] secs' %(ip,service_name,expired_time)
                else:
                    print "\033[31;1mNo data found in redis for service [%s] host [%s]\033[0m" %(service_name,ip)
        time.sleep(5)


def service_item_handle(main_ins,item_key,val_dict,client_service_data,ip):
    item_data = client_service_data['data'][item_key] #取出client对应服务器trigger的参数
    warning_val = val_dict['warning']
    critical_val = val_dict['critical']
    oper = val_dict["operator"]
    oper_func = getattr(operator,oper)

    if val_dict['data_type'] is float:
        item_data =float(item_data)
        warning_res = oper_func(item_data,warning_val)
        critical_res = oper_func(item_data,critical_val)
        print "warning:[%s] critical:[%s]" %(warning_val,critical_val)
        if critical_res:
            print u"\033[41;1mCRITICAL::\033[0mHost[%s] Service[%s] 阈值[%s] 当前值[%s],指标[%s]" %(
                client_service_data['host'],client_service_data['service'],critical_val,item_data,item_key
            )
        elif warning_res:
            print u"\033[42;1mWARNING::\033[0mHost[%s] Service[%s] 阈值[%s] 当前值[%s]" %(
                client_service_data['host'],client_service_data['service'],warning_val,item_data)
        else:
            print u"\033[32;2mSECURITY::\033[0mHost[%s] Service[%s] 当前值[%s]" %(
                    client_service_data['host'],client_service_data['service'],item_data)


