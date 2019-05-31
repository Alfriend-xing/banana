# coding=utf-8

import sys

from configparser import ConfigParser

from client_work import ClientWorker


cf = ConfigParser()
cf.read("banana.conf",encoding='utf-8')
server_type=cf['server type']['type']

def start():
    if server_type=='server':
        # 启动两个子进程
        pass
    elif server_type=='client':
        # 启动一个子进程
        work=ClientWorker()
        work.send()

def stop():
    # 查找并终止进程
    pass

def restart():
    stop()
    start()

if __name__=='__main__':
    option_type = sys.argv[1]
    if option_type == 'start':
        try:
            stop()
        except:
            pass
        start()
    elif option_type == 'stop':
        stop()
    elif option_type == 'restart':
        restart()
    else:
        print('[option error]\n start \n stop \n restart')


# todo
# ssserver是怎么启动，终止的
