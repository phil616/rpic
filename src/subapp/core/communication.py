import aiohttp
import ujson as json
from core.utils import get_ip
from typing import Dict
from conf import config
import requests
from pydantic import BaseModel
class RegisterSchema(BaseModel):
    authcode:str
    host:str
    port:int

    
port = 8000
url = "http://" + config.CP_HOST + ":" + str(port) + "/subapp"
async def login_to_command_pod():
    
    login_payload = {
        "authcode":config.AUTHCODE,
        "host":get_ip(),  # get ip
        "port":config.DEPLOY_PORT  # 
    }
    resp = requests.post(url=url + "/register",json=login_payload)
    if resp.status_code != 200:
        detail = resp.json().get("detail")
        if detail.get("type") == "subapp login exists":
            subapp_id = int(detail.get("id"))
            requests.get(url=url + "/remove?id="+str(subapp_id))    
            raise Exception(f"{subapp_id} has already exists, please retry.")
    return resp.json()

async def get_jwt_key()->Dict:
    jwt_info = requests.get(url=url+"/jwt")
    return jwt_info.json()