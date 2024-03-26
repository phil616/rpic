from base64 import b64encode,b64decode

def encode(data:bytes)->str:
    return str(b64encode(data))[2:-1]

def decode(data:str)->bytes:
    return b64decode(data)
