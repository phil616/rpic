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

from fastapi import FastAPI
from types import FunctionType
from core.logcontroller import log

server_process = None
def signal_handler(sig, frame):

    log.info("Server has been stopped by singal")
    if server_process is not None:
        server_process.should_exit = True

class MountingProcedure:
    def __init__(self,
                 app:FastAPI,
                 function:FunctionType,
                 endpoint:str,
                 params_number:int,
                 permissions:list,
                 group:str,
                 globals:dict
                 ):
        self.app = app
        self.function = function
        self.endpoint = endpoint
        self.params_number = params_number
        self.permissions = permissions
        self.group = group
        self.globals = globals
        
        # 