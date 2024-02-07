from typing import Dict, List, Union
from typing import Callable
from types import FunctionType
from formalize import ProcedureCodeObject
from dill import loads, dumps
from base64 import b64encode, b64decode

b = b'hello'
print(b.hex(":",2))
print(bytes.fromhex(b.hex()))

def f(r: int) -> int:
    print(r**2)
    def inner():
        print(r**3)
    return inner


class Serializer:
    """
    序列化器
    序列化器提供了一些工具类可以将对象序列化为字符串
    : input: 形式化的对象
    : output: 序列化的字符串
    """
    ...


class Deserializer:
    """
    反序列化器
    
    """
    ...

