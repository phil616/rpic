from fastapi import APIRouter,FastAPI
from pydantic import BaseModel
from fastapi import Request
from models.Subapp import Subapp
from conf import config
import datetime
from core.utils import get_current_time
from core.exceptions import HTTP_E403,HTTP_E401


class RegisterSchema(BaseModel):
    authcode:str
    host:str
    port:int


machine_router = APIRouter(prefix="/subapp")

@machine_router.post("/register")
async def subapp_login_register(info:RegisterSchema):
    if info.authcode!=config.SUBAPP_AUTHCODE:
        HTTP_E401("incorrect authcode")
    result = await Subapp.filter(subapp_host=info.host,subapp_port=info.port).all()
    if result:
          HTTP_E403(f"subapp exists{result}")
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

@machine_router.get("/release")
async def subapp_release_app(id:str):
    ...