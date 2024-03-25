from typing import Dict, List, Union
from typing import Callable
from types import FunctionType
from formalize import ProcedureCodeObject
from dill import loads, dumps
from base64 import b64encode, b64decode
from .formalize import ProcedureCodeObject
def f(r: int) -> int:
    print(r**2)
    def inner():
        print(r**3)
    return inner

def serialize(func_obj:ProcedureCodeObject)->bytes:
    return dumps(func_obj)

def Deserialize(func_bytes:bytes)->ProcedureCodeObject:
    return loads(func_bytes)

class Serializer:
    """
    DISABLED
    序列化器
    序列化器提供了一些工具类可以将对象序列化为字符串
    : input: 形式化的对象
    : output: 序列化的字符串
    """
    
    ...


class Deserializer:
    """
    DISABLED
    反序列化器
    
    """
    ...