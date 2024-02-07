

"""
The Compiler is turn python function's code object into a formalized object, and then turn it back to a function.
"""
from .formalize import ProcedureCodeObject
from typing import List, Union
from copy import deepcopy
from types import FunctionType, CodeType



def assemble_cp39(func:FunctionType, param: Union[List,None] = None):
    code_object = deepcopy(func.__code__)
    if not param:
        param = []
    return ProcedureCodeObject(**{
        "func_params": param,
        "argcount": code_object.co_argcount,
        "codestring": code_object.co_code,  # codestring and code are different with var names
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


def disassemble_cp39(obj: ProcedureCodeObject,global_vars: dict = None):
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
    ), globals().update(global_vars) if global_vars else globals()
    )


def exec_object(obj: ProcedureCodeObject):
    return disassemble_cp39(obj)(*obj.func_params)

