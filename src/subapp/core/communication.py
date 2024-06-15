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

import aiohttp
import ujson as json
from core.utils import get_ip
from core.dependencies import GlobalState
from typing import Dict
from conf import config
from core.logcontroller import logger as log
import requests
from pydantic import BaseModel
class RegisterSchema(BaseModel):
    authcode:str
    host:str
    port:int
    name:str
    type:int

    
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
async def login_to_root(aiohttp_session:aiohttp.ClientSession,state:GlobalState):
    """deprated"""
    jwt_key = None
    ROOT_URL = "http://" + "localhost:8000" + "/datahub/jwt"
    try:
        async with aiohttp_session.get(ROOT_URL) as response:
            resp = await response.json()
            log.info(f"JWT_KEY received from RPC_ROOT_SERVER: {resp}")
        jwt_key = resp.get("key","randomkey")
        jwt_algorithm = resp.get("algorithm", "HS256")

    except aiohttp.ClientConnectionError as e:
        log.exception(f"Failed to connect to RPC_ROOT_SERVER: {e}")

    if jwt_key:
        log.info(f"JWT_KEY received from RPC_ROOT_SERVER: {jwt_key}")
        state.runtime.set("JWT_KEY", jwt_key)
        state.runtime.set("JWT_DECRYPT", jwt_algorithm)
    else:
        state.runtime.set("JWT_KEY", "randomkey")
        state.runtime.set("JWT_DECRYPT", 'HS256')
        log.error("JWT_KEY not received from RPC_ROOT_SERVER, using default key: randomkey")
    
    # [GET GROUP NUMBER]0
        ...

def get_jwt_password()->dict:
    ROOT_URL = "http://" + "localhost:8000" + "/datahub/jwt"
    resp = requests.get(ROOT_URL)
    if resp.status_code == 200:
        return resp.json()
    """
    resp like: {"key":"xxx","algorithm":"xxx"}
    """