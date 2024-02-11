

class Cache(dict):
    def __init__(self,gid:int):
        self.gid = gid
    def get(self,key:str):
        return self.get(key)
    
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
    

