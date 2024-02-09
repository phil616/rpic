import rpyc
import jwt
from .cache import CachePool
from .disk import DiskPool

g_cache = CachePool()  # g_ means global or singleton
g_disk = DiskPool()

class SecuredService(rpyc.Service):
    """
    SecuredService class provides a secured service for RPC
    """
    def __init__(self,env_params:dict) -> None:
        self.decrypt_key = env_params.get("decrypt_key")
        self.decrypt_algorithm = env_params.get("decrypt_algorithm")
        super().__init__()
    def on_connect(self, conn):
        return super().on_connect(conn)
    def exposed_secured_op(self):
        
        return 'Secret String'
    
    def exposed_get_cache(self, key,token):
        gid = self.sys_get_group(token)
        return {"key":key, "group":gid}
    def exposed_cache_set(self, key, value, token):
        gid = self.sys_get_group(token)
        cache = self.get_cache(gid)
        cache.set(key, value)
        return {"key":key, "value":value, "group":gid}


    def on_disconnect(self, conn):
        return super().on_disconnect(conn)
    def sys_get_group(self,token:str):
        payload = jwt.decode(token, self.decrypt_key, algorithms=[self.decrypt_algorithm])
        return payload.get("gid")