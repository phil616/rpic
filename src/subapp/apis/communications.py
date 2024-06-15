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

