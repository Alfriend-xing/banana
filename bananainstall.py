# coding=utf-8
# 生成配置文件
import time
import sys
import os
import sqlite3

config=\
'''[general]
type=client
pidfile=banana.pid

# 客户端默认配置
[client]
# 客户端ID
client_id=%s
# 服务端IP
server_ip=127.0.0.1
# 数据发送端口
server_port=5000
# 发送间隔
second=1

# 服务端默认配置
[service]
# 内存CPU报警阀值
alarm=60
# 数据接收端口
data_port=5000
# web服务端口
web_port=5001'''


def write_cfg():
    id = str(int(round(time.time(),3)*1000))
    with open('banana.conf','w',encoding='utf-8') as f:
        f.write(config%id)

def find_db(db_name):
    db='db/db'+db_name+'.db'
    if os.path.exists(db):
        return True
    else:
        return False

def rm_db(db_name):
    db='db/db'+db_name+'.db'
    if os.path.exists(db):
        os.remove(db)
        return True
    else:
        return False

def get_dblist():
    path = os.getcwd()
    dbls=os.listdir(path+'/db')
    for i in dbls:
        if 'journal' in i:
            continue
        if i.startswith('db'):
            yield 'db/'+i

def create_database(db_name):
    db='db/db'+db_name+'.db'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    # 实时状态表
    c.execute('''CREATE TABLE realtime
             (id TEXT primary key, 
             platform TEXT, 
             ip TEXT, 
             updatetime TEXT, 
             cpu REAL, 
             mem TEXT,
             disk TEXT, 
             label TEXT, 
             message TEXT)''')

    # 所有主机共享一张历史表，在服务端进程中创建
    c.execute('''CREATE TABLE history 
             (id TEXT primary key, 
             updatetime TEXT, 
             cpu TEXT, 
             mem TEXT, 
             disk TEXT, 
             net TEXT)''')

    conn.commit()
    conn.close()



if __name__=='__main__':
    write_cfg()


# todo
# 如何生成系统服务文件，开机自启
# 如何生成系统服务 无需python启动


