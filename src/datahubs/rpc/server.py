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
from rpyc.utils.authenticators import AuthenticationError
from .tcp_multipart import decode,is_last_frame
from .rpc_service import SecuredService
import jwt


class ServiceFactory:
    def __init__(self,hostname:str,port:int,decrypt_key:str,decrypt_algorithm:str="HS256"):
        self.hostname = hostname
        self.port = port
        self.decrypt_key = decrypt_key
        self.decrypt_algorithm = decrypt_algorithm
        self.payload = {}
    def header_authenticator(self,sock):
        buffer = b''
        while True:
            buffer += sock.recv(1024)
            if is_last_frame(buffer):
                break
        decoded = decode(buffer)
        self.decrypt_jwt(decoded)
        return sock, None
    def decrypt_jwt(self,token):
        try:
            payload = jwt.decode(token, self.decrypt_key, algorithms=[self.decrypt_algorithm])
            print("crurent payload", payload)
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Token is not valid")
        except jwt.PyJWTError:
            raise AuthenticationError("Token parse failed")
        self.payload = payload
        return payload
    def make_thread_server(self,env_params:dict)->rpyc.ThreadedServer:
        env_params["decrypt_key"] = self.decrypt_key
        env_params["decrypt_algorithm"] = self.decrypt_algorithm
        env_params["payload"] = self.payload
        
        return rpyc.ThreadedServer(
            service=SecuredService(env_params), hostname=self.hostname,
            port=self.port, authenticator=self.header_authenticator
        )

def start_rpc_server(info_dict:dict):
    hostname = info_dict.get("hostname","localhost")
    port = info_dict.get("port",18812)
    decrypt_key = info_dict.get("decrypt_key","randomkey")
    decrypt_algorithm = info_dict.get("decrypt_algorithm","HS256")
    factory = ServiceFactory(hostname=hostname,port=port,decrypt_key=decrypt_key,decrypt_algorithm=decrypt_algorithm)
    server = factory.make_thread_server(env_params=info_dict)
    server.start()