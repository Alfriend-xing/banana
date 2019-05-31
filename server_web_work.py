# coding=utf-8
# 服务端

from flask import Flask,request

app=Flask(__name__)

# 首页 查询实时数据
@app.route('/',methods=['get'])
def index():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    for row in c.execute('SELECT * FROM realtime ORDER BY id'):
        print(row)
    conn.close()
    return 'ok'

# 主机详细信息

# 删除主机

# 添加 label 和 message

if __name__=='__main__':
    app.run(host='127.0.0.1',port=5001)








