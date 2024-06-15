
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


class Cache(dict):
    def __init__(self,gid:int):
        self.gid = gid
    def get(self,key:str):
        return self[key]
    
    def set(self,key:str,value):
        self[key] = value

    def delete(self,key:str):
        try:
            del self[key]
        except KeyError:
            pass

    def update(self,key:str,value):
        self[key] = value


class CachePool(dict):
    def __init__(self):
        self.cache_pool = {}
    def add_cache(self, cache: Cache):
        self.cache_pool[cache.gid] = cache
    def get_cache(self, gid:int):
        cache = self.cache_pool.get(gid)
        if not cache:
            cache = Cache(gid)
            self.add_cache(cache)
        return cache
    
    def delete_cache(self, gid:int):
        try:
            del self.cache_pool[gid]
        except KeyError:
            pass
    

