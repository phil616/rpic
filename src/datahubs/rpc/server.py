import rpyc
from rpyc.utils.authenticators import AuthenticationError
from tcp_multipart import decode,is_last_frame
from rpc_service import SecuredService
import jwt


class ServiceFactory:
    def __init__(self,hostname:str,port:int,decrypt_key:str,decrypt_algorithm:str="HS256"):
        self.hostname = hostname
        self.port = port
        self.decrypt_key = decrypt_key
        self.decrypt_algorithm = "HS256"
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
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Token is not valid")
        except jwt.PyJWTError:
            raise AuthenticationError("Token parse failed")
        return payload
    def make_thread_server(self)->rpyc.ThreadedServer:
        return rpyc.ThreadedServer(
            service=SecuredService, hostname=self.hostname,
            port=self.port, authenticator=self.header_authenticator
        )
