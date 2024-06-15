"""
开发者原创性与版权声明
该注释用于声明作者（开发者）具有该文件或代码的所有权利
作者承诺该源码具有原创性和唯一性
除法律约束的其他行为和上游协议外，该代码作者具有所有权利
作者承诺代码的原创性和完整性
作者：费东旭
最后一次更改日期：2024年6月10日（北京时间）
通讯地址：吉林省长春市朝阳区卫星路6543号长春大学计算机科学技术学院
通讯方式：phil616@163.com

"""

import threading
import os
import ujson as json
import warnings

class AbstractLocalStorage:
    """AbstractLocalStorage class is an abstract class for local storage.

    user can implement any local storage class by inheriting this class.
    like database proxy.
    """
    def set(self, key, value):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def remove(self, key):
        raise NotImplementedError
    
    def clear(self):
        raise NotImplementedError
    
    def submit(self):
        raise NotImplementedError
    
class CacheObject(AbstractLocalStorage):
    """CacheObject class can be regarded as a memory database.
    It is a singleton class, which means there is only one instance of it.

    Example:
        >>> cache = CacheObject('cache.json')
        >>> cache.set('key','value')
        >>> cache.get('key')
        'value'
        >>> cache.remove('key')
        >>> cache.get('key')
        None

    Attributes:
        _cache (dict): cache dictionary
        _mutex (threading.Lock): mutex lock
        _localdb (os.PathLike): local database file path

    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CacheObject, cls).__new__(cls)
        return cls._instance

    def __init__(self, localdb: os.PathLike = None) -> None:
        """Contructor of CacheObject class.
        Args:
            localdb (os.PathLike): local database file path
        """
        self._cache = dict()
        self._mutex = threading.Lock()
        self._localdb = localdb
        if self._localdb is not None:
            with self._mutex:
                self._load()

    def _load(self):
        if os.path.exists(self._localdb):
            with open(self._localdb) as f:
                self._cache = json.load(f)
        else:
            with open(self._localdb, 'w+') as f:
                json.dump(self._cache, f)

    def set(self, key, value):
        if key in self._cache:
            warnings.warn('Key already exists, will be overwritten.')
        self._cache[key] = value

    def get(self, key):
        if key not in self._cache:
            warnings.warn('Key not found.')
            return None
        return self._cache[key]

    def remove(self, key):
        if key not in self._cache:
            warnings.warn('Key not found.')
        del self._cache[key]

    def clear(self):
        self._cache.clear()

    def submit(self):
        if self._localdb is None:
            warnings.warn('Local database not specified.')
            return
        # with lock
        with self._mutex:
            with open(self._localdb, 'w+') as f:
                json.dump(self._cache, f)

    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, value):
        self.set(key, value)
        self.submit()
