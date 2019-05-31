# coding=utf-8
# 客户端

import psutil
import platform
import socket
from configparser import ConfigParser
import requests


class ClientWorker(object):
    def __init__(self):
        self.linuxsys=platform.linux_distribution()
        self.sys=[self.linuxsys[0],self.linuxsys[1]] if self.linuxsys[0] else\
             [platform.uname().system+platform.uname().release,platform.uname().version]
        self.ip=self.get_host_ip()
        self.read_config()

    def read_config(self):
        cf = ConfigParser()
        cf.read("banana.conf",encoding='utf-8')
        self.client_id=cf['client']['client_id']
        self.server_ip=cf['client']['server_ip']
        self.server_port=cf['client']['server_port']
        self.second=float(cf['client']['second'])

    def get_host_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    def get_msg(self):
        c=psutil.cpu_percent(interval=self.second, percpu=False)
        m=psutil.virtual_memory()
        ds=psutil.disk_partitions(all=False)
        d_total=0
        d_used=0
        for i in ds:
            try:
                tmp = psutil.disk_usage(i.mountpoint)
            except:
                continue
            else:
                d_total=d_total+tmp.total
                d_used=d_used+tmp.used
        d=round(d_used/d_total*100,2)
        return {
            'ip':self.ip,
            'platform':self.sys,
            'cpu':c,
            'mem':{'percent':m.percent,'used':int(m.used/1024**2),'total':int(m.total/1024**2)},
            'disk':{'percent':d,'used':int(d_used/1024**2),'total':int(d_total/1024**2)}
        }

    def send(self):
        for _ in range(100):
            self.send_api()
            # time.sleep(self.second)

    def send_api(self):
        url='http://'+self.server_ip+':'+self.server_port+'/'
        try:
            req=requests.post(url,json=self.get_msg(),timeout=1)
            print(req.text)
        except Exception as e:
            print(e)


if __name__=='__main__':
    # work=ClientWorker()
    # work.send()
    for k,v in psutil.net_io_counters(pernic=1, nowrap=True).items():
        print(k,v)