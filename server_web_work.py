# coding=utf-8
# 服务端

from flask import Flask,request,render_template
import sqlite3
import json

app=Flask(__name__)

# 首页 
@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')


# 查询实时数据api
@app.route('/api',methods=['get'])
def api():
    res=[]
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    for row in c.execute('SELECT * FROM realtime ORDER BY id'):
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

# 主机详细信息

# 删除主机

# 添加 label 和 message

if __name__=='__main__':
    app.run(host='127.0.0.1',port=5001)








