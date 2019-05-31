# coding=utf-8
# 服务端

from flask import Flask,request

app=Flask(__name__)

@app.route('/',methods=['POST'])
def receive_api():
    json=request.json
    print(json)
    return 'ok'


if __name__=='__main__':
    app.run(host='127.0.0.1',port=5000)








