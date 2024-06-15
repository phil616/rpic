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

# pycryptodome-3.20.0
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import hashlib
import bcrypt
import asyncio

"""
包含了哈希和加密
DONE
对于加密：提供AES加密和哈希加密
对于哈希：提供Bcrypt哈希加密和SHA256哈希加密
"""

class BasePassHash:
    _hash_source = None
    def passhash(self):
        raise NotImplementedError

    def verify(self):
        raise NotImplementedError

    async def async_passhash(self):
        raise NotImplementedError
    
    async def async_verify(self):
        raise NotImplementedError
class BaseCryption:
    _chiper = None
    _key = None
    def encrypt(self):
        raise NotImplementedError

    def decrypt(self):
        raise NotImplementedError
    
    async def async_encrypt(self):
        raise NotImplementedError
    
    async def async_decrypt(self):
        raise NotImplementedError
    
class AESCryption(BaseCryption):
    """

    """
    
    def __init__(self, mark: str):
        self._key = hashlib.sha256(bytes(mark, "utf-8")).hexdigest()[0:16]
        self._cipher = AES.new(self._key.encode('utf8'), AES.MODE_ECB)

    def encrypt(self, text: str) -> str:
        return self._cipher.encrypt(pad(bytes(text, "utf-8"), 32)).hex()

    def decrypt(self, text: str) -> str:
        return str(unpad(self._cipher.decrypt(bytes.fromhex(text)), 32), "utf8")

class SM4Cryption(BaseCryption):
    """
    Not Implemented
    """
    ...

class BcryptHash(BasePassHash):
    _hash_source = bcrypt
    def passhash(self, password: str) -> str:
        return self._hash_source.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify(self, password: str, hashed: str) -> bool:
        return self._hash_source.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    async def async_passhash(self, password: str) -> str:
        return await asyncio.to_thread(self.passhash, password)
    
    async def async_verify(self, password: str, hashed: str) -> bool:
        return await asyncio.to_thread(self.verify, password, hashed)
    
    
class SHA256Hash(BasePassHash):
    _hash_source = hashlib
    def passhash(self, password: str) -> str:
        return self._hash_source.sha256(password.encode("utf-8")).hexdigest()

    def verify(self, password: str, hashed: str) -> bool:
        return self._hash_source.sha256(password.encode("utf-8")).hexdigest() == hashed

    async def async_passhash(self, password: str) -> str:
        return await asyncio.to_thread(self.passhash, password)
    
    async def async_verify(self, password: str, hashed: str) -> bool:
        return await asyncio.to_thread(self.verify, password, hashed)
    
aes_encrypter = AESCryption("hello")

def encrypt(data:str)->str:
    return aes_encrypter.encrypt(data)

def decrypt(data:str)->str:
    return aes_encrypter.decrypt(data)