from fastapi import APIRouter,Depends
from core.dependencies import GlobalState,get_global_state
from core.exceptions import HTTP_E404,HTTP_E403
from core.logcontroller import logger
communication_router = APIRouter()

@communication_router.get("/group")
async def get_current_subapp_group_id(state:GlobalState=Depends(get_global_state)):
    gid = state.runtime.get("GROUP_ID")
    if not gid:
        HTTP_E404("No Group ID Assigned for now")
    logger.info(f"Group ID is $$GROUP_ID={gid}$$")
    return {"GROUP_ID":gid}


@communication_router.get("/assign/group")
async def assign_group_id_by_cp(gid:int,state:GlobalState=Depends(get_global_state)):
    gid = state.runtime.get("GROUP_ID")
    if gid:
        HTTP_E403(f"Group ID has been assgined $$GROUP_ID={gid}$$")
    state.runtime.set("GROUP_ID",gid)
    logger.info(f"ASSIGEND Group ID is $$GROUP_ID={gid}$$")
    return {"GROUP_ID":gid}

