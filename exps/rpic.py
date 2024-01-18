from typing import Union, Optional

from functools import wraps, reduce
from copy import deepcopy
from types import FunctionType, CodeType
from pydantic import BaseModel
from sys import version_info
from inspect import currentframe

class FunctionCodeObject(BaseModel):
    py_version: tuple = (version_info.major, version_info.minor)
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


def assemble(func, param: list):
    code_object = deepcopy(func.__code__)

    return FunctionCodeObject(**{
        "func_params": param,
        "argcount": code_object.co_argcount,
        "codestring": code_object.co_code,  # codestring and code are different with var names
        "cellvars": code_object.co_cellvars,
        "constants": code_object.co_consts,  # constants and consts are different with var names
        # "filename": code_object.co_filename,
        "filename": "<string>",
        "firstlineno": code_object.co_firstlineno,
        "flags": code_object.co_flags,
        "freevars": code_object.co_freevars,
        "posonlyargcount": code_object.co_posonlyargcount,
        "kwonlyargcount": code_object.co_kwonlyargcount,
        "lnotab": code_object.co_lnotab,
        "name": code_object.co_name,
        "names": code_object.co_names,
        "nlocals": code_object.co_nlocals,
        "stacksize": code_object.co_stacksize,
        "varnames": code_object.co_varnames,
    })

class Ob:
    def __init__(self):
        self.a = 1
    def print(self):
        print("Hello jee")

G_num = 3033  # 全局变量需要依靠filename来确定，那里进行了反编译，哪里的全局变量生效。


def disassemble(obj: FunctionCodeObject):

    globaldict = globals()
    globaldict['ob'] = Ob()
    return FunctionType(CodeType(
        obj.argcount,
        obj.posonlyargcount,
        obj.kwonlyargcount,
        obj.nlocals,
        obj.stacksize,
        obj.flags,
        obj.codestring,
        obj.constants,
        obj.names,
        obj.varnames,
        __name__,  # filename，这里可能需要frame来确定全局环境变量
        obj.name,
        obj.firstlineno,
        obj.lnotab,
        obj.freevars,
        obj.cellvars,
    ),globaldict )


def exec_object(obj: FunctionCodeObject):
    return disassemble(obj)(*obj.func_params)


r = 10
def hello():
    ob.print()
    print("hello")

ret = assemble(hello,[])
disassemble(ret)()

def reference():
    print("hello reference")

reference()
del reference