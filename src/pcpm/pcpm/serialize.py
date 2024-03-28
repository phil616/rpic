
from formalize import ProcedureCodeObject
from dill import loads, dumps


def serializer(func_obj:ProcedureCodeObject)->bytes:
    return dumps(func_obj)

def deserializer(func_bytes:bytes)->ProcedureCodeObject:
    return loads(func_bytes)
