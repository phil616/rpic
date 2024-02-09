import rpyc
import jwt
class SecuredService(rpyc.Service):
    def on_connect(self, conn):
        return super().on_connect(conn)
    def exposed_secured_op(self):
        return 'Secret String'
    def exposed_get_cache(self, key, token):
        gid = self.sys_get_group(token)
        return {"key":key, "group":gid}
    def on_disconnect(self, conn):
        return super().on_disconnect(conn)
    def sys_get_group(self,token:str):
        payload = jwt.decode(token, "randomkey", algorithms=["HS256"])
        return payload.get("gid")