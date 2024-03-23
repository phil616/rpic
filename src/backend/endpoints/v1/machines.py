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
