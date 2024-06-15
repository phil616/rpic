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

from fastapi import APIRouter,FastAPI
from pydantic import BaseModel
from fastapi import Request
from models.Subapp import Subapp
from conf import config
import datetime
from core.utils import get_current_time
from core.exceptions import HTTP_E403,HTTP_E401
"""
this file has been deprated
"""

class RegisterSchema(BaseModel):
    authcode:str
    host:str
    port:int


machine_router = APIRouter(prefix="/subapp")

@machine_router.post("/register")
async def subapp_login_register(info:RegisterSchema):
    if info.authcode!=config.SUBAPP_AUTHCODE:
        HTTP_E401("incorrect authcode")
    result = await Subapp.filter(subapp_host=info.host,subapp_port=info.port).first()
    if result:
          HTTP_E403({"message:":f"subapp exists{result}",
                     "type":"subapp login exists",
                     "id":result.subapp_id}
                     )
    else:
        new_subapp = await Subapp.create(subapp_host=info.host,
                      subapp_port=info.port,
                      subapp_status=True,
                      subapp_latest_report=get_current_time()
                      )
        return new_subapp

@machine_router.get("/flush")
async def subapp_flush_status(id:str):
    subapp = await Subapp.filter(subapp_id=id).first()
    subapp.subapp_latest_report = get_current_time()
    await subapp.save()
    return {"success":"ok"}

@machine_router.get("/remove")
async def subapp_remove_app(id:str):
    current_app = await Subapp.filter(subapp_id=id).first()
    await current_app.delete()
    return {"status":"ok"}

@machine_router.get( "/jwt"
                    #,dependencies=[Security(check_permissions, scopes=["datahub"])]
                    )
async def get_datahub_info():
    return {"key":config.JWT_SECRET_KEY, "algorithm":config.JWT_ALGORITHM}
