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

import uuid
import random
import typing
"""
format
BOUNDARYUUIDUUIDUUIDUUID [bounary header] + [uuid*4] (8+16 = 24 bytes) 1024-24 = 1000
HAS NEXT [has next] (2 byte)  998 
CURRENT FRAME LENGTH [length] (4 bytes (1~994) )  994
CONTENT [content] (length bytes) 994 padding with 0
BOUNDARYUUIDUUIDUUIDUUID [bounary header] + [uuid*4] (8+16 = 24 bytes)
"""

def get_uuid(lengtn:int=16) -> bytes:
    """
    get uuid function provide a upper case uuid string
    like 8A2B3C4D5E6F7G8H9I0J1K2L3M4N5O6P
    :param lengtn: the length of the uuid string less than 16
    :return: uuid string
    """
    if lengtn > 16:
        raise ValueError("lengtn should be less than 16")
    return uuid.uuid4().__str__().upper().replace('-', '').encode()[:lengtn]
def generate_ramdom_body(length=1024):
    """
    generate a random bytes body with length, used for test
    :param length: the length of the body
    :return: random bytes
    """
    body = b''
    for i in range(length):
        body += random.Random().randint(0, 255).to_bytes(1, 'big')
    return body

class TCPMultipart:
    """
    TCPMultipart is a class to generate rpyc's multipart data package

    TCP Multipart is a protocol used by rpyc to transfer large data, for bytes data transfer,
    rpyc's client and server use the same protocol, every package is 1024 bytes, it looks like:
    for every package:
    Boundary part: 24 bytes 
    it consist of 8 bytes "BOUNDARY" and 16 bytes uuid: BOUNDARYUUIDUUIDUUIDUUID
    extra:the word "BOUNDARY" is a fixed word, the uuid is a random uuid string
    
    Has next part: 2 bytes
    it consist of 2 bytes, if it is the last package, it will be 00, else 01

    Current frame length: 4 bytes
    it consist of 4 bytes, it is the length of the content part, the max length is 994

    Content part: 994 bytes
    it consist of 994 bytes, the content of the package
    if the content is less than 994, it will be padding with 0
    """
    def __init__(self,body:bytes,boundary:bytes=b"BOUNDARY"):
        """
        init function
        given a body and a boundary, generate a TCPMultipart object
        :param body: the body of the package
        :param boundary: the boundary of the package, it has to a word with 8 bytes
        """
        self.body = body
        self.body_length = len(body)
        boundary_id = get_uuid(16)
        self.boundary = boundary + boundary_id
        self.boundary_length = len(self.boundary)
        self.has_next = b'00'
        self.current_frame_length = b'0000'
    @staticmethod
    def split_bytes(data, chunk_size):
        """
        split a bytes data into chunks with chunk_size
        :param data: the bytes data you want to split
        :param chunk_size: length of the chunk
        :return: list of chunks
        """
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        return chunks

    def export_package(self):
        """
        export the package, generate the package with the body
        :return: the package
        """
        chunks = self.split_bytes(self.body, 994)
        last_chunk_length = len(chunks[-1])
        padding_length = 994 - last_chunk_length
        padding = b'0' * padding_length
        result = b''
        for c in chunks:
            current_frame_length = len(c).to_bytes(4, 'big')
            if c != chunks[-1]:
                has_next = b'01'
            else:
                has_next = b'00'
            if c == chunks[-1]:
                c += padding
            result += self.boundary + has_next + current_frame_length + c
        return result

def decode(data:bytes):
    chunk_size = 1024
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    result = b''
    last_boundary = b''
    for chunk in chunks:
        print(len(chunk))
        boundary = chunk[:24]
        last_boundary = boundary
        if last_boundary != boundary:
            raise ValueError('boundary not match')
        has_next = chunk[24:26]
        current_frame_length = chunk[26:30]
        if has_next == b'00':
            result += chunk[30:30+int.from_bytes(current_frame_length, 'big')]
        else:
            result += chunk[30:]
    return result   
def is_last_frame(data:bytes):
    return data[24:26] == b'00'
"""
RPICUUIDUUIDID content[1565] RPICUUIDUUIDID
RPICUUIDUUIDID content[1024-14]
content[351] padding RPICUUIDUUIDID
"""

def tests():
    o = generate_ramdom_body(128*2)
    tcp = TCPMultipart(o)
    r = tcp.export_package()
    print(r)
    with open("export.bin","wb") as f:
        f.write(r)
    print(decode(r))
    if o == decode(r):
        print('OK')
if __name__ == '__main__':
    tests()