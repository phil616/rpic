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

"""
This file(endpoints) has following ORM operation
User CURD
"""
from fastapi import APIRouter, Security
from typing import Optional
from core.authorize import check_permissions
from models.User import User
from models.Group import Group
from models.GroupUser import GroupUser
from core.exceptions import HTTP_E401
from models.RoleScope import RoleScope

from pydantic import BaseModel
from core.logcontroller import log
from core.proxy import request # state is a contextvar
user_router = APIRouter(prefix="/user",dependencies=[Security(check_permissions,scopes=["USER:CURD"])])

async def curd_get_user_all_info(uid:int)->dict:
    """
    CURD functions
    get user all info by user id
    :param uid: user id
    :return: dict
    """
    result_set = {
        "user_basic":{},
        "user_info":{},
        "user_roles":[],
        "permissions":[],
        "groups":[],
        "group_admins":[],
    }
    target_user = await User.filter(user_id=uid).first()
    result_set.update({"user_basic":{
        "uid":target_user.user_id,
        "username":target_user.username,
        "status":target_user.user_status,
    }})
    result_set.update({"user_info":target_user.user_info})
    user_roles = target_user.user_roles.split(",")
    result_set.update({"user_roles":user_roles})
    permissions = [] 
    for role in user_roles:
        role_scopes = await RoleScope.filter(user_role=role).first()
        permissions.extend(role_scopes.role_scopes.split(","))
    result_set.update({"permissions":permissions})
    group_admins = await Group.filter(group_administrator=target_user.user_id).all()
    result_set.update({"group_admins":group_admins})
    groups = await GroupUser.filter(user_id=target_user.user_id).all()
    result_set.update({"groups":groups})
    return result_set

# USER retrive R
@user_router.get("/get/info")
async def user_get_userinfo_by_id(uid:Optional[int]=None):
    if uid is None:
        uid = request.userinfo.get("uid")
    user = await User.filter(user_id=request.userinfo.get("uid")).first()
    if user.user_id != uid:
        # check login user has permission to get other user's info
        group = await Group.filter(group_administrator=user.user_id).first()
        users_in_current_group = await GroupUser.filter(group_id=group.group_id).all()
        for group_user in users_in_current_group:
            if user.user_id != group_user.user_id:
                #401
                HTTP_E401("the user you get not in your group")
    result = await curd_get_user_all_info(uid)
    log.debug(f"get user info: {result} by user {request.userinfo.get('uid')}")
    return result
class UserBasicSchema(BaseModel):
    username: str
    password: str
    user_info: dict
    user_roles: str
    user_status: int

# USER create C
@user_router.post("/create")
async def user_create_user(user:UserBasicSchema):
    """
    CURD functions
    create user
    :param user: UserCreateSchema
    :return: dict
    """
    user = await User.create(
        username=user.username,
        password=user.password,
        user_info=user.user_info,
        user_roles=user.user_roles,
        user_status=user.user_status
    )
    return user

# User update U
@user_router.post("/update")
async def user_update_user(uid:int,user:UserBasicSchema):
    """
    CURD functions
    update user
    :param uid: user id
    :param user: UserCreateSchema
    :return: dict
    """
    user = await User.filter(user_id=uid).update(
        username=user.username,
        password=user.password,
        user_info=user.user_info,
        user_roles=user.user_roles,
        user_status=user.user_status
    )
    return user

# User D
@user_router.post("/delete")
async def user_delete_exist_user(uid:int):
    """
    CURD functions
    delete user
    :param uid: user id
    :return: dict
    """
    user = await User.filter(user_id=uid).delete()
    return user

@user_router.get("/all")
async def user_curd_get_all_user():
    users = await User.all()
    return users