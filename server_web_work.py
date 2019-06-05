# coding=utf-8
# 服务端

from flask import Flask,request,render_template
import sqlite3
import json
from bananainstall import get_dblist

app=Flask(__name__)

# 首页 
@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')


# 查询实时数据api
@app.route('/api',methods=['get'])
def api():
    res=[]
    for i in get_dblist():
        conn = sqlite3.connect(i)
        c = conn.cursor()
        row=c.execute('SELECT * FROM realtime WHERE id=?',(i[5:-3],)).fetchone()        
        res.append({
            'id':row[0],
            'platform':row[1],
            'ip':row[2],
            'updatetime':row[3],
            'cpu':row[4],
            'mem':row[5],
            'disk':row[6],
            'label':row[7],
            'message':row[8]
        })
        conn.close()
    return json.dumps(res)

# 查询历史API
@app.route('/api/history/<id>',methods=['get'])
def api_history(id):
    res=[]
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    history_res = c.execute('SELECT * FROM history WHERE id=?',(id,)).fetchone()
    if history_res:
        return json.dumps({'state':True,
                            'id':history_res[0],
                            'updatetime':eval(history_res[1]),
                            'cpu':eval(history_res[2]),
                            'mem':eval(history_res[3]),
                            'disk':eval(history_res[4]),
                            'net':eval(history_res[5]),
                            })
    else:
        return json.dumps({'state':False})
    conn.close()


# 删除主机
@app.route('/api/delete',methods=['post'])
def api_delete():
    data=request.form
    id=data['id']
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    res = c.execute('SELECT * FROM realtime WHERE id=?',(id,)).fetchone()
    if res:
        sql='DELETE FROM realtime WHERE ID =?'
        c.execute(sql,(id,))
        conn.commit()
    else:
        return json.dumps({"state":False})
    res = c.execute('SELECT * FROM history WHERE id=?',(id,)).fetchone()
    if res:
        sql='DELETE FROM history WHERE ID =?'
        c.execute(sql,(id,))
        conn.commit()
    else:
        return json.dumps({"state":False})
    conn.close()
    return json.dumps({"state":True})

# 添加 label 和 message
@app.route('/api/msg',methods=['post'])
def api_msg():
    data=request.form
    id=data['id']
    label=data['label']
    msg=data['message']
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    res = c.execute('SELECT * FROM history WHERE id=?',(id,)).fetchone()
    if res:
        sql='''
        UPDATE realtime SET 
                    label=?,
                    message=?
                    WHERE id=?'''
        c.execute(sql,(label,msg,id))
        conn.commit()
        conn.close()
        return json.dumps({"state":True})
    else:
        return json.dumps({"state":False}),500

if __name__=='__main__':
    app.run(host='127.0.0.1',port=5001)








