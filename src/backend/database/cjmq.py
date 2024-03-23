# Cache JSON MQ
from aioredis import Redis
#from conf import config
import aioredis
from typing import Optional,List
from queue import Queue
import redis
import ujson as json
import datetime
import asyncio
from threading import Lock
class CJMQBaseExceptions(Exception):
    ...

class CJMQUninitializedError(CJMQBaseExceptions):
    ...

class CJMQLockFailed(CJMQBaseExceptions):
    ...
class CJMQIOBase:
    def __init__(self,uri:Optional[str]="redis://localhost") -> None:
        self.__redis_uri:str = uri
        self._redis:Redis = None
        self._lock_key:str = 'SHARED_LOCK'
        self._max_attempt:int = 3
        self._db_index = 0
        self._init = False
    async def aio_init(self):
        cache_pool = aioredis.ConnectionPool.from_url(
            self.__redis_uri,
            db=self._db_index,
        )
        self._redis = Redis(connection_pool=cache_pool)
        self._init = True


    async def _acquire_lock(self):
        if not self._init:
            raise CJMQUninitializedError
        acquired = await self._redis.setnx(self._lock_key, 'LOCKED')
        if acquired:
            return True
        else:
            return False
    async def _release_lock(self):
        await self._redis.delete(self._lock_key)
    async def get(self,key):
        return await self._redis.get(key)
    async def set(self,key,value,*args,**kwargs):
        if not self._init:
            raise CJMQUninitializedError
        
        attempts = 0
        while attempts < self._max_attempt:
            if await self._acquire_lock():
                try:
                    await self._redis.set(key,value,*args,**kwargs)
                finally:
                    # 释放锁
                    await self._release_lock()
                    return None
            else:
                attempts += 1
        raise CJMQLockFailed("Too many attempts to get redis lock")
    
    async def close(self):
        await self._redis.close()

class CJMQMessage:
    def __init__(self) -> None:
        self.payload:str = None
        self.expire:float = None
        self.id:int = None
    
class CJMQSynchronizer:
    def __init__(self,uri:Optional[str]="redis://localhost") -> None:
        self._db_index = 0
        self.__redis_uri = uri
        cache_pool = aioredis.ConnectionPool.from_url(
            self.__redis_uri,
            db=self._db_index,
        )
        self._redis = Redis(connection_pool=cache_pool)
        self.repo = "queue"
        self.queue = []
        self.mutex = Lock()
        self.sync_task=None
    async def synchronize(self):
        while True:
            all_elem = await self._redis.get(self.repo)
            raw = str(all_elem)
            all_elem:List[CJMQMessage] = json.loads(raw)
            self.mutex.acquire()
            self.queue.clear()
            for elem in all_elem:
                if elem.expire <= datetime.datetime.now().timestamp():
                    # should be remove
                    continue
                self.queue.append(elem)
            self.mutex.release()
            asyncio.sleep(0.2)
    def start(self):
        self.sync_task = asyncio.create_task(self.synchronize(self))
    def stop(self):
        self.sync_task.cancel()  # i dont know if it will work, i dont want to write test case

    def input(self):
        ...
    def remove(self):
        ...
    def show(self):
        ...