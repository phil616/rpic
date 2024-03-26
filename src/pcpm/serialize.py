from typing import Dict, List, Union
from typing import Callable
from types import FunctionType
from formalize import ProcedureCodeObject
from dill import loads, dumps
from base64 import b64encode, b64decode
from formalize import ProcedureCodeObject
def f(r: int) -> int:
    print(r**2)
    def inner():
        print(r**3)
    return inner

def serializer(func_obj:ProcedureCodeObject)->bytes:
    return dumps(func_obj)

def deserializer(func_bytes:bytes)->ProcedureCodeObject:
    return loads(func_bytes)
