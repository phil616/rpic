import rpyc
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
    jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjEsInBlciI6W10sImdpZCI6MSwiZXhwIjoxNzA3NTU3MjM5LCJpc3MiOiJSUElDUyBCYWNrZW5kIn0.LsGVqJZeXFb0qyaHc2vjPifOcMBH_HZr89HRbzpb4yg"
    tcp = TCPMultipart(jwt.encode())
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
jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjEsInBlciI6W10sImdpZCI6MSwiZXhwIjoxNzA3NTU3MjM5LCJpc3MiOiJSUElDUyBCYWNrZW5kIn0.LsGVqJZeXFb0qyaHc2vjPifOcMBH_HZr89HRbzpb4yg"
    
print(conn1.root.get_cache('key',jwt))
exit(0)
