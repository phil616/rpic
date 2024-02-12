from fastapi import APIRouter,Depends,Security
from dataobj import sqlobj
from webcore.dependenices import GlobalState, get_global_state
from webcore.authorize import check_permissions


http_interface_router = APIRouter(prefix="/sql",dependencies=[Security(check_permissions,scopes=["PROCEDURE:ADMIN"])])

async def http_interface_disk_delete(sql:str, state:GlobalState=Depends(get_global_state)):
    result = sqlobj.execute_sql(sql, state.user.get("gid"))
    return result

http_interface_router.post("/execute")(http_interface_disk_delete)