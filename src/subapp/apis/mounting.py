from fastapi import APIRouter,Depends,FastAPI
from core.dependencies import GlobalState,get_global_state
from core.exceptions import HTTP_E404,HTTP_E403
from fastapi.requests import Request
from pydantic import BaseModel
from core.logcontroller import logger
from conf import config
from pcpm.testcase import r_cp39_object as test_callable_test
mounting_router = APIRouter(prefix="/mount")

def mount_router_to_app(app:FastAPI,function:callable,path:str):
    logger.info(f"Mounting {function} to path: {path}")
    app.add_api_route(path=path,endpoint=function,methods=["POST","GET"])

class MountSchema(BaseModel):
    body:str # callable body
    path:str # path to mount
    userspace:str

@mounting_router.post("/endpoint")
async def mount_endpoint(
    mount_schema:MountSchema,
    req:Request,
    global_state:GlobalState=Depends(get_global_state)
    ):
    if not config.APP_DEBUG:
        callable_body = mount_schema.body
    else:
        callable_body = test_callable_test
    path = mount_schema.userspace + "/" + mount_schema.path
    mount_router_to_app(req.app,callable_body,path)
    return {"status":"success"}

