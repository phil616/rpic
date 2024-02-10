from fastapi import APIRouter
from pydantic import BaseModel
from models.Group import Group
from fastapi import Request,Depends
from typing import Optional,Dict
from core.runtime import get_global_state
from fastapi import Security
from core.authorize import check_permissions
from models.User import User
from models.GroupUser import GroupUser
group_router = APIRouter(prefix="/group",dependencies=[Security(check_permissions,scopes=["GROUP:CURD"])])


class GroupSchema(BaseModel):
    group_name : str
    group_info : Optional[Dict] = {}
    group_status : Optional[int] = 1
@group_router.post("/create")
async def create_group_by_schema(group:GroupSchema,state = Depends(get_global_state)):
    """
    """
    creator_id = state.user.get("uid")
    current_group = await Group.create(group_administrator=creator_id,group_name=group.group_name,group_info=group.group_info,group_status=group.group_status)
    return current_group

@group_router.get("/get/all")
async def get_all_groups():
    all_groups = await Group.all()
    return all_groups

@group_router.get("/get/{group_id}")
async def get_group_by_id(group_id:int):
    current_group = await Group.filter(group_id=group_id).first()
    return current_group

@group_router.post("/update/{group_id}")
async def update_group_by_id(group_id:int,group:GroupSchema):
    raise NotImplementedError
    ...

@group_router.get("/addUser")
async def add_user_to_group_by_uid(uid:int,state = Depends(get_global_state)):
    current_group = await Group.filter(group_administrator=state.user.get("uid")).first()
    gu = GroupUser.create(user_id=uid,group_id=current_group.group_id)
    return gu

