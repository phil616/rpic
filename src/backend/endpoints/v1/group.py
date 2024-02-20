"""
This file(endpoints) has following ORM operation
Group CURD
GroupUser CURD
"""
from fastapi import APIRouter
from pydantic import BaseModel
from models.Group import Group
from fastapi import Depends
from typing import Optional,Dict
from core.runtime import get_global_state
from fastapi import Security
from core.authorize import check_permissions
from core.logcontroller import log
from models.User import User
from models.GroupUser import GroupUser
from core.proxy import request as state  # state is a contextvar
group_router = APIRouter(prefix="/group",dependencies=[Security(check_permissions,scopes=["GROUP:CURD"])])


class GroupSchema(BaseModel):
    group_name : str
    group_info : Optional[Dict] = {}
    group_status : Optional[int] = 1

# GROUP create C
@group_router.post("/create")
async def group_create_group(group:GroupSchema):
    """
    """
    creator_id = state.user.get("uid")
    user = await User.filter(user_id=creator_id).first()
    log.debug(f"current user is {creator_id}")
    log.debug(f"following datas will insert:{creator_id,group.group_name,group.group_info,group.group_status}")
    current_group = await Group.create(
        group_administrator=user,
        group_name=group.group_name,
        group_info=group.group_info,
        group_status=group.group_status)
        
    return current_group

# GROUP update U
@group_router.post("/update")
async def group_update_group():
    ...

# GROUP Retrive R
@group_router.get("/get")
async def group_get_info():
    ...

# Group Delete D
@group_router.get("/delete")
async def group_delete_group():
    ...

# GROUP Retirve R All
@group_router.get("/get/all")
async def group_get_group_all():
    all_groups = await Group.all()
    return all_groups


# GROUPUSER Create C
@group_router.get("/user/create")
async def group_user_add_user_to_group(uid:int,state = Depends(get_global_state)):
    current_group = await Group.filter(group_administrator=state.user.get("uid")).first()
    user = await User.filter(user_id=uid).first()
    gu = await GroupUser.create(group_id=current_group,user_id=user)
    return gu

# GROUPUSER Update u
@group_router.get("/user/update")
async def group_user_update():
    ...

# GROUPUSER Retrive R
@group_router.get("/user/get/all")
async def group_user_get_current_group_user(state = Depends(get_global_state)):
    my_id = state.user.get("uid")
    my_group = await Group.filter(group_administrator=my_id).first()
    all_users_in_my_group = await GroupUser.filter(group_id=my_group).all()
    log.debug(all_users_in_my_group)
    return all_users_in_my_group


# GROUPUSER Delete D
@group_router.get("/user/delete")
async def group_user_delete():
    ...
