"""
NOT Finished 
"""
from rpyc import Service
from rpyc.core.protocol import Connection

from rpyc.utils.authenticators import AuthenticationError

def magic_word_authenticator(sock):
    if sock.recv(5) != "abcde":
        raise AuthenticationError("wrong magic word")
    return sock, None

class AuthenticatedService(Service):
    def __init__(self, usr,pwd):
        self.username = usr
        self.password = pwd

    def on_connect(self, conn:Connection):
        # 在连接建立时执行身份验证
        if not self.authenticate(conn):
            print(conn)
            raise Exception("Authentication failed")

    def authenticate(self, conn:Connection):
        return True
        # 执行身份验证逻辑，例如检查用户名和密码是否匹配
        # 这里只是一个简单的示例，你可以根据实际需求进行定制
        credentials = conn._config['credentials']
        print("**********",credentials)
        print("=======",conn._config)
        if credentials and credentials.get('username') == self.username and credentials.get('password') == self.password:
            return True
        return False

    def exposed_add(self, x, y):
        return x + y

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    server = ThreadedServer(AuthenticatedService("my_token","my_password"), port=18861,authenticator=magic_word_authenticator)
    server.start()