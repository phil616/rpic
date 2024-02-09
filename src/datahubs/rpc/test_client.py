import rpyc
import traceback
from tcp_multipart import TCPMultipart
# solved by https://stackoverflow.com/questions/69917561/how-to-implement-username-password-authenticator-for-rpyc-server


class AuthSocketStream(rpyc.SocketStream):
    @classmethod
    def connect(cls, *args, authorizer=None, **kwargs):
        stream_obj =  super().connect(*args, **kwargs)

        if callable(authorizer):
            authorizer(stream_obj.sock)

        return stream_obj

def callback_authorizer(sock):
    tcp = TCPMultipart(b'23')
    r = tcp.export_package()
    sock.send(r)
def rpyc_connect(host, port, service=rpyc.VoidService, config={}, ipv6=False, keepalive=False, authorizer=None):
    s = AuthSocketStream.connect(
            host, port, ipv6=ipv6, keepalive=keepalive,
            authorizer=authorizer
    )

    return rpyc.connect_stream(s, service, config)

print('With correct authorizer')

conn1 = rpyc_connect(
        'localhost', 18812, authorizer=callback_authorizer
)

print(conn1.root.secured_op())
exit(0)
print('With wrong authorizer')

conn2 = rpyc_connect(
        'localhost', 18812, authorizer=lambda sock: sock.send('Invalid'.encode())
)

try:
    conn2.root
except Exception:
    print(traceback.format_exc())


print('With no authorizer')

conn3 = rpyc_connect(
        'localhost', 18812
)

try:
    conn3.root
except Exception:
    print(traceback.format_exc())