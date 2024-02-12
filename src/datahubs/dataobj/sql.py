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
事实证明在常规的LRU中，双链表性能好的原因是指针对内存随机访问的时间复杂度是O(1).
但模拟双链表的顺序表在Python中的性能并不好，因为顺序表的插入和删除操作的时间复杂度是O(n)。

因此采用维持一个优先列表来代替双链表。

"""
import sqlite3
import threading
from os import PathLike
from os.path import join,dirname
from typing import Any,Dict

class PriorityList(list):
    def __init__(self,maxlen:int):
        super().__init__()
        self.maxlen = maxlen
        self._ddl = []

    def add(self, element:Any)->int:
        """append element to tail and return element's index in list"""
        if len(self._ddl) >= self.maxlen:
            self._ddl.pop(0)
        self._ddl.append(element)   
        return len(self._ddl)-1

    def remove(self,idx:int):
        self._ddl.pop(idx)

    def swap(self,idx1:int,idx2:int):
        self._ddl[idx1],self._ddl[idx2] = self._ddl[idx2],self._ddl[idx1]

    def __getitem__(self, idx:int):
        return self._ddl[idx]
    

class SQLiteConnection:
    def __init__(self,sqlite_path:PathLike,max_connections:int=10):
        self.sqlite_path = sqlite_path
        self.max_connections = max_connections
        self.lock = threading.Lock()

        self.lru_stack = PriorityList(max_connections)
        self.lru_cache:Dict[str,int] = {}

    def _create_connection(self,user:str) -> sqlite3.Connection:
        conn_name = join(self.sqlite_path,user+".sqlite")
        return sqlite3.connect(conn_name)
    
    def get_connection(self,user:str) -> sqlite3.Connection:
        with self.lock:
            user_cache_idx:int = self.lru_cache.get(user)
            if user_cache_idx is None:
                new_conn = self._create_connection(user)
                idx = self.lru_stack.add(new_conn)
                self.lru_cache[user] = idx
                return new_conn
            else:
                conn = self.lru_stack[user_cache_idx]
                self.lru_stack.remove(user_cache_idx)
                new_idx = self.lru_stack.add(conn)
                self.lru_cache[user] = new_idx
                return conn
    def close_connection(self,user:str):
        with self.lock:
            user_cache_idx:int = self.lru_cache.get(user)
            if user_cache_idx is not None:
                conn = self.lru_stack[user_cache_idx]
                conn.close()
                self.lru_stack.remove(user_cache_idx)
                self.lru_cache.pop(user)
    def close_all_connections(self):
        with self.lock:
            for conn in self.lru_stack:
                conn.close()
            self.lru_stack.clear()
            self.lru_cache.clear()
    def __del__(self):
        self.close_all_connections()

SQL_PATH = join(dirname(dirname(__file__)),"storage")
SQL_CONN = SQLiteConnection(SQL_PATH,10)

def execute_sql(sql:str,userspcae:str):
    conn = SQL_CONN.get_connection(userspcae)
    cursor = conn.cursor()
    cursor.execute(sql)

    all = cursor.fetchall()
    

    conn.commit()
    cursor.close()
    SQL_CONN.close_connection(userspcae)