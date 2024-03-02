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