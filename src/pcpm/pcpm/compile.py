

"""
BASIC COMPLETE
The Compiler is turn python function's code object into a formalized object, and then turn it back to a function.
"""
from formalize import ProcedureCodeObject
from typing import List, Union
from copy import deepcopy
from types import FunctionType, CodeType
from typing import Literal
from dill import loads, dumps

"""
Procedure,Function,Script的区别

Procedure: 一个过程，是一个执行过程的函数，不允许闭包，可以被挂在到一个Endpoint上
Function: 一个函数，允许闭包，但不能使用全局变量，不能被挂载到Endpoint上
Script: 一个脚本，允许闭包，直接执行

| 类型      | 是否允许闭包 | 是否允许全局变量 | 是否携带参数  |挂载到端点 |  最终目标形式  |
| --------- | ------------ | ---------------- | ---------- | ---------- | -------------- |
| Procedure | 否           | 是               | 是         | 是         |  codeobject raw |
| Function  | 是           | 否               | 否         |  dill package   |
| Script    | 是           | 是               | 否         |  str raw        |

"""

def assemble_cp39(func:FunctionType, param: Union[List,None] = None):
    code_object = deepcopy(func.__code__)
    if not param:
        param = []
    return ProcedureCodeObject(**{
        "func_params": param,
        "argcount": code_object.co_argcount,
        "codestring": code_object.co_code,  # codestri00ng and code are different with var names
        "cellvars": code_object.co_cellvars,
        "constants": code_object.co_consts,  # constants and consts are different with var names
        "filename": code_object.co_filename,
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


class Assemble:
    def __init__(self,name:str="anoymous",func_type:Literal["Script","Function","Procedure"] = "Function") -> None:
        self.procedure_name:str = name
        self.procedure_type:Literal["Script","Function","Procedure"] = func_type
        self.result: bytes = None

    def assemble(self,func:Union[FunctionType,str], param: Union[List,None] = None):
        if self.procedure_type == "Procedure":
            procedure_raw_object = assemble_cp39(func,param)
            self.result = dumps(procedure_raw_object)
        elif self.procedure_type == "Function":
            self.result = dumps(func)
        elif self.procedure_type == "Script":
            self.result = func.encode("utf-8")
        else:
            raise ValueError("Unknown Procedure Type")
        return self.result

def disassemble_cp39(obj: ProcedureCodeObject,global_vars: dict = None):
    print(obj)
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
        obj.filename,
        obj.name,
        obj.firstlineno,
        obj.lnotab,
        obj.freevars,
        obj.cellvars,
    ), 
    globals().update(global_vars) if global_vars else globals()
    )

class Disassemble:
    def __init__(self,object_infos:dict) -> None:
        self.procedure_name:str = object_infos.get("name","anoymous")
        self.procedure_type:Literal["Script","Function","Procedure"] = object_infos.get("type","Function")
    def disassemble(self,object:bytes,global_vars:dict = None)->Union[ProcedureCodeObject,FunctionType,str]:
        if self.procedure_type == "Procedure":
            procedure_raw_object = loads(object)
            return disassemble_cp39(procedure_raw_object,global_vars)
        elif self.procedure_type == "Function":
            return loads(object)
        elif self.procedure_type == "Script":
            return object.decode("utf-8")
        else:
            raise ValueError("Unknown Procedure Type")



def exec_object(obj: ProcedureCodeObject):
    return disassemble_cp39(obj)(*obj.func_params)

