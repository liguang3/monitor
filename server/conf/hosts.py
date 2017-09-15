#!/usr/bin/env python
#coding:utf-8
import templates
#from core import  redishelper
web_clusters = templates.LinuxGenericTemplate()
web_clusters.hosts=['192.168.2.230',
                    '192.168.4.2',
                    '34.45.33.45']
mysql_groups = templates.LinuxGenericTemplate()
mysql_groups.hosts = [
    '192.168.1.2',
    '192.168.1.4'

]
monitored_groups = [mysql_groups]


if __name__ =='__main__':
    host_config_dic = {}
    for group in  monitored_groups:
       # print group.name
        for h in group.hosts:#循环主机组里的机器
            if h not in host_config_dic:#给每台主机生成一个配置字典
                host_config_dic[h]={}
            #print hosts,group.services
            for s in group.services:
                host_config_dic[h][s.name] = [s.plugin_name,s.interval]#把服务添加到主机配置字典里
                #print  host_config_dic
