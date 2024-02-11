import sqlite3
import threading
from os import PathLike
class SQLiteConnection:
    def __init__(self,sqlite_path:PathLike,max_connections:int=10):
        self.sqlite_path = sqlite_path
        self.max_connections = max_connections
        self.lru_stack = None
        self.lock = threading.Lock()



"""
对于一个嵌入到RPC服务中的SQL对象而言，一个线程同一时间只能获取到一个磁盘IO，
因此磁盘IO设计为多线程并发是没有意义的，只能在节省对象开销上下功夫。
对于一个sqlite连接来说，连接对象需要被创建，创建后连接磁盘IO，然后执行SQL操作，最后关闭连接。
这个过程是串行的过程，因此需要设计一个连接池来尽可能复用这些sqlite连接对象。
但对于带有用户鉴权的RPC服务来说，需要保障用户空间的隔离性，因此每个用户都会分到一个独立的连接。
为了能够复用连接，需要LRU算法来实现连接管理中心。
对于一个连接管理中心而言，其输入是用户的用户空间名称，输出是一个SQL连接对象。
LRU算法可以保障频繁使用的连接不会被关闭，而不频繁使用的连接会被关闭。

对于连接管理中心而言，内部维持一个固定大小的连接栈，当用户请求连接时，要么从栈中取出一个连接，要么创建一个新连接。
不论连接从何而来，最新的连接都会被放到栈顶，而最老的连接会被放到栈底。

在Python中实现双链表的难度很低，但Python不支持指针，
因此指针在Python中是以对象的形式存在的。
而Python的对象处理开销很大，直接模拟双链表会有极大的性能问题。

因此，需要用顺序表来模拟双链表。
来源于Acwing第827题：双链表
https://www.acwing.com/activity/content/problem/content/864/


"""
