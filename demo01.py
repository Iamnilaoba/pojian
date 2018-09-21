# # 3. 使用多线程写一个一对一聊天的服务器
# import gevent
# from gevent import socket,monkey
# def aa(Socket):
#     while True:
#         data=Socket.recv(1024)
#         print("收到了客户的请求："+data.decode("utf-8"))
#         Socket.send(b'我收到了')
# serverSocket=socket.socket()
# serverSocket.bind(("127.0.0.1",9999))
# serverSocket.listen()
# while True:
#     clientSocket,add=serverSocket.accept()
#     a=gevent.spawn(aa,clientSocket)
#
#
# # 4. 使用进程、线程、协程分别写出一个生产者和消费者模式
# from multiprocessing import JoinableQueue,Process
# def product(queue,name):
#     for i in range(10):
#         queue.put(name)
#         print("生产了一个苹果")
#         queue.join()
# def cur(queue):
#     while True:
#         r=queue.get()
#         print("吃了一个："+r)
#         queue.task_done()
# if __name__ == '__main__':
#     queue=JoinableQueue()
#     p1=Process(target=product,args=(queue,"苹果"))
#     p2=Process(target=cur,args=(queue,))
#     p2.a=True
#     p1.start()
#     p2.start()
#     p2.join()
#
#
# # 6. 使用多进程写一个web服务器，可以返回给浏览器json串（注意content-type）
#
# from flask import  Flask
# from flask import make_response
# import json
#
# app=Flask(__name__)
# @app.route("/login",methods=["POST","GET"])
# def login():
#     dic={}
#     dic["code"]=200
#     dic["msg"]="登陆成功"
#     dic["data"]=[{"name":"xiaoming","age":12}]
#     resp=make_response(json.dumps(dic))
#     resp.headers['Content-Type']="applocation/json:charset=utf-8"
#     return resp
#
# if __name__ == '__main__':
#     app.run()


import threading
import time
def eat() :
    lockA.acquire() # 上锁了
    currentThread = threading.currentThread() # 获取到当前的线程
    print("%s 使用lockA上锁了" %currentThread.name)
    time.sleep(0.1)
    lockB.acquire() # 使用B上锁
    currentThread = threading.currentThread()
    print("%s 使用lockB上锁了 " %currentThread.name)
    lockB.release()
    lockA.release()  # 释放锁

def eat1() :
    lockB.acquire()  # 使用B上锁
    currentThread = threading.currentThread()
    print("%s 使用lockB上锁了 " % currentThread.name)
    time.sleep(0.1)
    lockA.acquire()  # 上锁了
    currentThread = threading.currentThread()  # 获取到当前的线程
    print("%s 使用lockA上锁了" % currentThread.name)
    lockA.release()  # 释放锁
    lockB.release()

lockA = threading.Lock() # 锁1
lockB = threading.Lock() # 锁2
AA = threading.Thread(target=eat,name="AA")
BB = threading.Thread(target=eat1,name="BB")
AA.start()
BB.start()




lst3 = [
        {"name": "张三", "habby": "吸烟"},
        {"name": "张三", "habby": "烫头"},
        {"name": "张三", "habby": "早恋"},
        {"name": "张三", "habby": "喝酒"},
        {"name": "李四", "habby": "写代码"},
        {"name": "李四", "habby": "看博客"},
    ]

le = len(lst3)
i = 0
while i < le :
    dic = lst3[i]
    j = i + 1
    while j < le:
        dict = lst3[j]
        if dic["name"] == dic ['name']:
            if type (dic['hebby']) is list:
                dic['hebby'].append(dict['hebby'])
                del lst3[j]
                le -= 1
            else:
                q = []
                q.append(dic['hebby'])
                dic['hebby'] = q
                dic['hebby'].append(dict['hebby'])
                del lst3[j]
                le -= 1
        else:
            j += 1
    i += 1
print(lst3)










