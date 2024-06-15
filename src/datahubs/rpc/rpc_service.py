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

import rpyc
import jwt
from dataobj import g_disk,g_cache

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