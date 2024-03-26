from pydantic import BaseModel
from sys import version_info
from typing import Optional
class ProcedureCodeObject(BaseModel):
    py_version: Optional[tuple] = (version_info.major, version_info.minor)
    func_params: list = []
    argcount: int = 0
    posonlyargcount: int = 0
    kwonlyargcount: int = 0
    nlocals: int = 0
    stacksize: int = 0
    flags: int = 0
    codestring: bytes = b''
    constants: tuple = ()
    names: tuple = ()
    varnames: tuple = ()
    filename: str = ''
    name: str = ''
    firstlineno: int = 0
    lnotab: bytes = b''
    freevars: tuple = ()
    cellvars: tuple = ()

