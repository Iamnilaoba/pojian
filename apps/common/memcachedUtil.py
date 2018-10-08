# Memcached是一个高性能的分布式内存对象缓存系统，用于动态WEB应用以减轻数据库负载。它通过在内存中缓存数据
# 和对象来减少读取数据库的次数，从而提高动态，数据库网站的速度。Memcached基于一个存储键/值对的hashmap。
# 其守护进程（daemon）是用C写的，但是客户端可以用任何语言来编程，并通过memcached协议与守护进程通信。
import memcache

mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def saveCache(key,value,time=0) :
    mc.set(key=key,val=value,time=time)

def getCache(key):
    return mc.get(key)

def delete(key):
    mc.delete(key)
