import aiohttp
import ujson as json
from core.utils import get_ip
from conf import config
import requests
from pydantic import BaseModel
class RegisterSchema(BaseModel):
    authcode:str
    host:str
    port:int

async def login_to_command_pod(session:aiohttp.ClientSession):
    
    login_payload = {
        "authcode":config.AUTHCODE,
        "host":get_ip(),  # get ip
        "port":config.DEPLOY_PORT  # 
    }

    port = 8000
    url = "http://" + config.CP_HOST + ":" + str(port) + "/subapp" + "/register"
    session.headers.add("content_type","application/json")
    async with session.post(url, json=login_payload) as response:
        return await response.json()