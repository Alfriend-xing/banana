# coding=utf-8
# 服务端

from flask import Flask,request
from concurrent.futures import ThreadPoolExecutor 
import sqlite3
from threading import Lock
import time
import json

app=Flask(__name__)
pool = ThreadPoolExecutor(200)
lock=Lock()

@app.route('/api/',methods=['POST'])
def receive_api():
    json_data=request.json
    # pool.submit(thread_sql,json_data)
    return thread_sql(json_data)
    # if json_data['type']=='second':
    #     return thread_sql(json_data)
    # elif json_data['type']=='hour':
    #     pass
    # else:
    #     return 'data error'

@app.route('/api/history/',methods=['POST'])
def receive_history_api():
    json_data=request.json
    return thread_history_sql(json_data)

def thread_sql(json_data):
    # lock.acquire()
    # 加锁不会丢数据 一条4秒；不加锁丢一半数据，一条2秒
    # print('-'*60+json_data['id']+'-'*20)
    try:
        conn = sqlite3.connect('test.db',timeout=1)
        c = conn.cursor()
        t1 = (str(json_data['id']),)
        t2=(json_data['platform'],
            json_data['ip'],
            str(json_data['updatetime']),
            json_data['cpu'],
            json.dumps(json_data['mem']),
            json.dumps(json_data['disk']),)
        real_res=c.execute('SELECT * FROM realtime WHERE id=?', t1).fetchone()
        if real_res:
            sql='''UPDATE realtime SET 
                    platform=?,
                    ip=?,
                    updatetime=?,
                    cpu=?,
                    mem=?,
                    disk=?
                    WHERE id=?'''
            c.execute(sql,t2+t1)
        else:
            sql='''INSERT INTO realtime VALUES (?,?,?,?,?,?,?,?,?)'''
            c.execute(sql,t1+t2+('',''))
            # sql='''CREATE TABLE "%s"
            #     (updatetime TEXT primary key, 
            #     cpu REAL, 
            #     mem TEXT, 
            #     disk TEXT)'''
            # table_name='history'+json_data['id']
            # c.execute(sql%table_name)
        conn.commit()
        return 'True'
    except Exception as e:
        conn.rollback()
        print(type(e))
        print(e)
        return 'False'
    finally:
        # lock.release()
        conn.close()

def thread_history_sql(json_data):
    # 向历史表格插入数据
    # lock.acquire()
    # 加锁不会丢数据 一条4秒；不加锁丢一半数据，一条2秒
    # print('-'*60+json_data['id']+'-'*20)
    try:
        conn = sqlite3.connect('test.db',timeout=1)
        c = conn.cursor()
        t1 = (str(json_data['id']),)
        t2=(str(json_data['updatetime']),
            json_data['cpu'],
            json.dumps(json_data['mem']),
            json.dumps(json_data['disk']),
            json.dumps(json_data['net']),)
        real_res=c.execute('SELECT * FROM history WHERE id=?', t1).fetchone()
        if real_res:
            tmp=[]
            for i in range(1,7):
                tmp.append(str(eval(real_res[i])[1:]+[t2[i-1]]))    # so bad

            sql='''UPDATE realtime SET 
                    updatetime=?,
                    cpu=?,
                    mem=?,
                    disk=?,
                    net=? 
                    WHERE id=?'''
            c.execute(sql,tuple(tmp)+t1)
        else:
            sql='''INSERT INTO history VALUES (?,?,?,?,?,?)'''
            tmp=[None]*9 # 999 测试时存10条，生产环境1000
            c.execute(sql,t1+(str(tmp+[i]) for i in t2))
        conn.commit()
        return 'True'
    except Exception as e:
        conn.rollback()
        print(type(e))
        print(e)
        return 'False'
    finally:
        # lock.release()
        conn.close()

if __name__=='__main__':
    app.run(host='127.0.0.1',port=5000)


# todo
# 数据库操作放入子线程中
# 数据类型修正
# 记录历史数据





