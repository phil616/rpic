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
from loguru import logger as log
import ujson as json

class SQLiteConnection:
    def __init__(self,raw_connection:sqlite3.Connection,userspace:str):
        log.debug(f"SQLiteConnection created for userspace {userspace}")
        self.raw_connection = raw_connection
        self.userspace = userspace
    def __del__(self):
        self.raw_connection.close()
        self.userspace = None

class SQLiteConnectionPriorityList:
    def __init__(self,sqlite_path:PathLike,maxlen:int):
        super().__init__()
        log.debug(f"SQLiteConnectionPriorityList created with maxlen {maxlen}")
        self.maxlen = maxlen
        self._lru_list = []
        self._lru_cache = {}
        self.sqlite_path = sqlite_path
        self.lock = threading.Lock()
    def _create_connection(self,userspace:str)->SQLiteConnection:
        log.debug(f"SQLiteConnection {userspace} is created")
        conn_name = join(self.sqlite_path,userspace+".userspace.sqlite")
        return SQLiteConnection(sqlite3.connect(conn_name),userspace)
    def get_connection(self,userspace:str)->SQLiteConnection:
        connection:SQLiteConnection = self._lru_cache.get(userspace)  # Union[None,SQLiteConnection]
        if connection:
            # cache hit
            return self._lru_list[connection]
        else:
            # cannot find connection in cache
            # create a new connection
            with self.lock:
                if len(self._lru_list) >= self.maxlen:
                    # cache pool is full
                    # pop the last connection
                    poped_connection:SQLiteConnection = self._lru_list.pop(0)
                    user = poped_connection.userspace
                    log.debug(f"SQLiteConnection {user} is poped from cache")
                    self._lru_cache.pop(user)  # remove the connection from cache
                    del poped_connection
                    new_connection:SQLiteConnection = self._create_connection(userspace)
                    self._lru_list.append(new_connection)
                    new_connection_idx = len(self._lru_list)-1
                    self._lru_cache[userspace] = new_connection_idx
                    return new_connection

                else:
                    new_connection:SQLiteConnection = self._create_connection(userspace)
                    self._lru_list.append(new_connection)
                    new_connection_idx = len(self._lru_list)-1
                    self._lru_cache[userspace] = new_connection_idx
                    return new_connection
    def remove_connection(self,userspace:str):
        connection:SQLiteConnection = self._lru_cache.get(userspace)
        if connection is not None:
                popped = self._lru_list.pop(connection)
                self._lru_cache.pop(userspace)
                del popped
    def clear(self):
        for conn in self._lru_list:
            conn.raw_connection.close()
        self._lru_list.clear()
        self._lru_cache.clear()
    def __del__(self):
        self.clear()
    

SQL_PATH = join(dirname(dirname(__file__)),"storage")
SQL_CONN = SQLiteConnectionPriorityList(SQL_PATH,10)

def execute_sql(sql:str,userspcae:str):
    conn = SQL_CONN.get_connection(userspcae).raw_connection
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    # conn.close()  # in cache pool, connection should not be closed
    json_data = json.dumps(rows)
    return json_data
