import rpyc
from rpyc.utils.authenticators import AuthenticationError
from tcp_multipart import decode,is_last_frame
def header_authenticator(sock):
    buffer = b''
    while True:
        buffer += sock.recv(1024)
        if is_last_frame(buffer):
            break
    decoded = decode(buffer)
    if decoded != b"23":
        raise AuthenticationError("Username and password is not correct")
    return sock, None

class SecuredService(rpyc.Service):
    def exposed_secured_op(self):
        return 'Secret String'

rpyc.ThreadedServer(
    service=SecuredService, hostname='localhost',
    port=18812, authenticator=header_authenticator,
).start()