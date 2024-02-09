import uuid
import random
"""
format
BOUNDARYUUIDUUIDUUIDUUID [bounary header] + [uuid*4] (8+16 = 24 bytes) 1024-24 = 1000
HAS NEXT [has next] (2 byte)  998 
CURRENT FRAME LENGTH [length] (4 bytes (1~994) )  994
CONTENT [content] (length bytes) 994 padding with 0
BOUNDARYUUIDUUIDUUIDUUID [bounary header] + [uuid*4] (8+16 = 24 bytes)
"""

def get_uuid(lengtn=16) -> bytes:
    if lengtn > 16:
        raise ValueError("lengtn should be less than 16")
    return uuid.uuid4().__str__().upper().replace('-', '').encode()[:lengtn]
def generate_ramdom_body(length=1024):
    body = b''
    for i in range(length):
        body += random.Random().randint(0, 255).to_bytes(1, 'big')
    return body
class TCPMultipart:
    def __init__(self,body:bytes,boundary:bytes=b"BOUNDARY"):
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
        将字节流按指定长度分割
        :param data: 要分割的字节流
        :param chunk_size: 分割的长度
        :return: 分割后的字节流列表
        """
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        return chunks

    def export_package(self):
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
    o = generate_ramdom_body(1024*2)
    tcp = TCPMultipart(o)
    r = tcp.export_package()
    print(r)
    print(decode(r))
    if o == decode(r):
        print('OK')
