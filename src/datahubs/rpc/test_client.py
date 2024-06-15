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
