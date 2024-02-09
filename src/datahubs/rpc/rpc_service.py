import rpyc
from rpc_cachedb import SystemCache
cache = SystemCache()
class SecuredService(rpyc.Service):
    def on_connect(self, conn):
        r = conn.recv(2048)
        print(r)
        return super().on_connect(conn)
    def exposed_secured_op(self):
        return 'Secret String'
    
    def on_disconnect(self, conn):
        return super().on_disconnect(conn)
