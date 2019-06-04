# coding=utf-8
# 生成配置文件
import time
import sys
import os
import sqlite3

client_config=\
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
second=1'''

server_config=\
'''[general]
type=server
pidfile=banana.pid

# 服务端默认配置
[service]
# 内存CPU报警阀值
alarm=60
# 数据接收端口
data_port=5000
# web服务端口
web_port=5001'''

def client_install():
    id = str(int(round(time.time(),3)*1000))
    with open('banana.conf','w',encoding='utf-8') as f:
        f.write(client_config%id)

def server_install():
    if os.path.exists('test.db'):
        os.remove('test.db')
    conn = sqlite3.connect('test.db')
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
             cpu REAL, 
             mem TEXT, 
             disk TEXT, 
             net TEXT)''')

    conn.commit()
    conn.close()
    with open('banana.conf','w',encoding='utf-8') as f:
        f.write(server_config)


if __name__=='__main__':
    if len(sys.argv)<=1:
        print('[option error]\n client \n server ')
        sys.exit()
    else:
        install_type = sys.argv[1]
    if install_type == 'client':
        client_install()
    elif install_type == 'server':
        server_install()
    else:
        print('[option error]\n client \n server ')


# todo
# 如何生成系统服务文件，开机自启
# 如何生成系统服务 无需python启动


