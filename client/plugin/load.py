#!/usr/bin/env python
# encoding: utf-8
"""@version: ??
@author: Daven Li
@file: load.py
@time: 2017/8/15 8:09
"""
#!/usr/bin/env python
# encoding: utf-8
"""@version: ??
@author: Daven Li
@file: cpu.py
@time: 2017/8/15 8:09
"""
import commands
def monitor(first_invoke=1):
    shell_command = 'uptime'
    status,result = commands.getstatusoutput(shell_command)
    if status != 0:
        value_dic = {'status':status}
    else:
        value_dic={}
        uptime = result.split(',')[:1][0]
	load1,load5,load10 = result.split('load average:')[1].split(',')
        value_dic['data_value']={
            'uptime':uptime,
            'load1':load1,
            'load5':load5,
           'load10':load10,
            'status':status
        }
    return value_dic
if __name__ == '__main__':
    print monitor()
