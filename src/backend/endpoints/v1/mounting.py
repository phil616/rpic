from fastapi import APIRouter,Depends, Security
from pydantic import BaseModel,Field
from typing import List,Literal,Dict,Optional,Union,Sequence
from models.Procedure import Procedure
from models.Group import Group
from models.EndpointProcedure import EndpointProcedure
from core.authorize import check_permissions
from core.runtime import get_global_state,GlobalState
from core.exceptions import HTTP_E404,HTTP_E401
import asyncio
from core.logcontroller import log
from fastapi import Request
import requests
from core.proxy import request
class MountingSchema(BaseModel):
    path:str
    methods:Literal["GET","POST"] = Field(default="POST")
    procedure_id:int

def get_available_subapp(
        subapps:List[Dict],
        gid:int
        )->Union[None,Dict]:
    prefix = "http://"  # can be switch to https
    """
    subapp list structure demo
    [
        {
            "type": "Service Pod",
            "port": 8001,
            "host": "10.1.175.242"
        }
    ]

    BASIC LOGIC:
    1. searching existing subapp
      if exist, return
      else 
      2. if has available subapp is not assigned
        has empty sp: assign and return
        else 
        failed
    """
    empty_sequence = []
    for app in subapps:
        url = f"{prefix}{app.get('host')}:{app.get('port')}/group"
        log.info(f"Sendingg GET {url}")
        resp = requests.get(url)
        log.info(f"resp is {resp.status_code}")
        if resp.status_code == 404:
            empty_sequence.append(app)
        if resp.status_code == 200:
            group_id = resp.json().get("GROUP_ID")
            if gid == group_id:
                return app
    if len(empty_sequence) == 0:
        log.info("no subapp is can use")
        return None
    else:
        for unassign_app in empty_sequence:
            log.info(f"trying {unassign_app}")
            resp = requests.get(f"{prefix}{unassign_app.get('host')}:{unassign_app.get('port')}/assign/group?gid={gid}")
            if resp.status_code == 200:
                log.info(f"resp 200ok! {resp.text}")
                return unassign_app
            else:
                log.error(resp.text)

async def mount():
    ...
mounting_router = APIRouter(prefix="/mounting",dependencies=[Security(check_permissions,scopes=["GROUP:ENDPOINT"])])
@mounting_router.get("/subapp")
async def get_all_avaliable_subapp(
    state:GlobalState=Depends(get_global_state)):
    gid = request.userinfo.get("gid") 
    if not gid:
        HTTP_E401("Group Field required")
    subapps :List = state.runtime.get("sp")
    if not subapps:
        HTTP_E404("No availiable subapp services for serve")
    subapp = get_available_subapp(subapps,gid)
    return subapp
    
@mounting_router.post("/mount")
async def mount_subapp(
    schema:MountingSchema,
    state:GlobalState=Depends(get_global_state)):
    gid = request.userinfo.get("gid")
    if gid is None:
        HTTP_E401("Group Field required")
    for char in schema.path:
        if char == "/":
            HTTP_E401("Path can't contain /")
    # mounting a pid -> endpoints

    # get current users' group
    group = await Group.filter(group_id=gid).first()
    p = await Procedure.filter(procedure_id=schema.procedure_id).first()
    # check if the mount path is already exist
    existence = await EndpointProcedure.filter(
        namespace=group.group_name,
        mount_path=schema.path,
        ).first()
    if existence:
        HTTP_E401("Mount path is already exist")

    # add EndPoint to Procedure mapping
    mapping = await EndpointProcedure.create(
        procedure_id=schema.procedure_id,
        namespace=group.group_name,
        mount_path=schema.path,
    )

    subapps :List = state.runtime.get("sp")
    if not subapps:
        HTTP_E404("No availiable subapp services for assigend")

    subapp = get_available_subapp(subapps,gid)
    if not subapp:
        HTTP_E401("No availiable subapp services for serve")



    # let subapp mount this procedure
    subapp_url = f"http://{subapp.get('host')}:{subapp.get('port')}/mount/endpoint"
    
    resp = requests.post(subapp_url,json={
        "body":p.procedure_raw,
        "path":schema.path,
        "userspace":group.group_name
    })
    if resp.status_code == 200:
        return mapping

    # apply to nginx center

    return mapping