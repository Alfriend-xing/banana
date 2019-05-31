# coding=utf-8
# 服务端

from flask import Flask,request

app=Flask(__name__)

@app.route('/',methods=['POST'])
def receive_api():
    json_data=request.json
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    t1 = (json_data['id'],)
    t2=(json_data['platform'],
        json_data['ip'],
        json_data['updatetime'],
        json_data['cpu'],
        json_data['mem'],
        json_data['disk'],)
    real_res=c.execute('SELECT * FROM realtime WHERE id=?', t1).fetchone()
    if real_res:
        sql='''UPDATE realtime SET 
                platform=?,
                ip=?,
                updatetime=?,
                cpu=?,
                mem=?,
                disk=?,
                WHERE id=?'''
        c.execute(sql,t2+t1)
    else:
        sql='''INSERT INTO realtime VALUES (?,?,?,?,?,?,?)'''
        c.execute(sql,t1+t2)
        sql='''CREATE TABLE %s
             (updatetime TEXT primary key, 
             cpu REAL, 
             mem TEXT, 
             disk TEXT)'''
        c.execute(sql%history+str(json_data['id']))
    conn.commit()
    conn.close()
    return 'ok'


if __name__=='__main__':
    app.run(host='127.0.0.1',port=5000)


# todo
# 数据库操作放入子线程中
# 数据类型修正





