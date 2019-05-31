# coding=utf-8

import os,sys,signal
from multiprocessing import Process
import time

from configparser import ConfigParser

from client_work import ClientWorker


cf = ConfigParser()
cf.read("banana.conf",encoding='utf-8')
server_type=cf['general']['type']
pidfile=cf['general']['pidfile']

def write_pid(pids):
    print(pids)
    with open(pidfile,'w') as f:
        for pid in pids:
            f.write(str(pid)+' ')

def start():
    if os.path.exists(pidfile):
        print('is running')
        stop()
    if server_type=='server':
        # 启动两个子进程
        p1=Process(target=testtask)
        p1.start()
        p2=Process(target=testtask)
        p2.start()
        write_pid([p1.pid,p2.pid])
    elif server_type=='client':
        # 启动一个子进程
        work=ClientWorker()
        # p1=Process(target=work.send)
        p1=Process(target=testtask)
        p1.start()
        write_pid([p1.pid])
        sys.exit()
    print('started')

def stop():
    # 查找并终止进程
    if not os.path.exists(pidfile):
        print('isn\'t running')
        return
    with open(pidfile,'r') as f:
        pids=f.readline().strip().split(' ')
        for pid in pids:
            try:
                os.kill(int(pid.strip()),1)
            except SystemError:
                continue
            except Exception as e:
                print(type(e))
    os.remove(pidfile)
    print('stopped')

def restart():
    stop()
    start()

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
    option_type = sys.argv[1]
    if option_type == 'start':
        start()
    elif option_type == 'stop':
        stop()
    elif option_type == 'restart':
        restart()
    else:
        print('[option error]\n start \n stop \n restart')


# todo
# ssserver是怎么启动，终止的
