# coding=utf-8

import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor ,wait
pool = ThreadPoolExecutor(100)

s=time.time()
t=0
f=0

def task(i):
    for _ in range(60):
        data={
                # "id":str(int(round(time.time(),3)*1000)),
                "id":str(i),
                "ip":"127.0.0.1",
                "platform":"win10",
                "cpu":random.randint(1,100),
                "mem":{"percent":random.randint(1,100),"used":90,"total":100},
                "disk":{"percent":random.randint(1,100),"used":90,"total":100},
                "updatetime":int(time.time())
            }
        global t,f
        res=requests.post("http://127.0.0.1:5000/",json=data)
        print(res.text)
        if res.text=="True":
            t=t+1
        else:
            f=f+1
        time.sleep(1)

taskpool=[]
for i in range(5):
    taskpool.append(pool.submit(task,i))
wait(taskpool)
e=time.time()
print(e-s)
print("t:",t)
print("f:",f)