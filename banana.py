# coding=utf-8

import os,sys,signal
from multiprocessing import Process
from threading import Thread
import time

from configparser import ConfigParser

from client_work import ClientWorker
from server_data_work import app as data_app
from server_web_work import app as web_app


cf = ConfigParser()
cf.read("banana.conf",encoding='utf-8')
server_type=cf['general']['type']

def start():
    if server_type=='server':
        data_port=cf['service']['data_port']
        web_port=cf['service']['web_port']
        # 启动两个子线程
        p1=Thread(target=data_app.run,kwargs={'host':'0.0.0.0','port':data_port})
        p1.setDaemon(True)
        p1.start()
        web_app.run(host='0.0.0.0',port=web_port)
    elif server_type=='client':
        # 启动一个子线程
        work=ClientWorker()
        work.send()

def testtask():#task
    try:
        # task()
        while True:
            print(time.time())
            time.sleep(1)
    except:
        pass
    finally:
        stop()


if __name__=='__main__':
    start()


# todo
# ssserver是怎么启动，终止的
