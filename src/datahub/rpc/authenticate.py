import rpyc

class AuthenticatedService(rpyc.Service):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def on_connect(self, conn):
        # 在连接建立时执行身份验证
        if not self.authenticate(conn):
            raise Exception("Authentication failed")

    def authenticate(self, conn):
        # 执行身份验证逻辑，例如检查用户名和密码是否匹配
        # 这里只是一个简单的示例，你可以根据实际需求进行定制
        credentials = conn._config.get('credentials')
        if credentials and credentials.get('username') == self.username and credentials.get('password') == self.password:
            return True
        return False

    def exposed_add(self, x, y):
        return x + y

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    username = "your_username"
    password = "your_password"
    server = ThreadedServer(AuthenticatedService(username, password), port=18861)
    server.start()