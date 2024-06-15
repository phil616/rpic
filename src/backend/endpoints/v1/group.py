"""
This file(endpoints) has following ORM operation
Group CURD
GroupUser CURD
"""
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
from core.proxy import request   # state is a contextvar

group_router = APIRouter(prefix="/group",
                         dependencies=[
                             Security(check_permissions,scopes=["GROUP:CURD"])
                         ])

class GroupSchema(BaseModel):
    group_name : str
    group_info : Optional[Dict] = {}
    group_status : Optional[int] = 1

# GROUP create C
@group_router.post("/create")
async def group_create_group(group:GroupSchema):
    """创建一个组
    """
    creator_id = request.userinfo.get("uid")
    user = await User.filter(user_id=creator_id).first()
    log.debug(f"current user is {creator_id}")
    log.debug(f"following datas will insert:{creator_id,group.group_name,group.group_info,group.group_status}")
    current_group = await Group.create(
        group_administrator=user.user_id,  # 管理员
        group_name=group.group_name,       # 组名称
        group_info=group.group_info,       # 组信息
        group_status=group.group_status)   # 组状态
        
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
    """查询所有组"""
    all_groups = await Group.all()
    return all_groups


# GROUPUSER Create C
@group_router.get("/user/create")
async def group_user_add_user_to_group(uid:int):
    """
    添加用户到当前组
    Args:
        uid:要添加的用户
    """
    current_group = await Group.filter(group_administrator=request.userinfo.get("uid")).first()  # 获取登录的用户
    user = await User.filter(user_id=uid).first()  # 要添加的用户
    gu = await GroupUser.create(group_id=current_group.group_id,user_id=user.user_id)
    return gu

# GROUPUSER Update u
@group_router.get("/user/update")
async def group_user_update():
    ...

# GROUPUSER Retrive R
@group_router.get("/user/get/all")
async def group_user_get_current_group_user():
    """
    获取当前用户所在组的所有用户
    """
    my_id = int(request.userinfo.get("uid"))
    my_group = await Group.filter(group_administrator=my_id).first()
    all_users_in_my_group = await GroupUser.filter(group_id=my_group.group_id).all()
    log.debug(all_users_in_my_group)
    return all_users_in_my_group


# GROUPUSER Delete D
@group_router.get("/user/delete")
async def group_user_delete():
    ...
