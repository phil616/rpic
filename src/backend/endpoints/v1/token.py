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

from typing import Annotated
from fastapi import APIRouter,Depends
from core.authorize import OAuth2WithGroupRequest, create_access_token
from core.exceptions import HTTP_E401
from curd.authentication import verify_password, get_user_permissions
from models.User import User
from models.GroupUser import GroupUser
from models.Group import Group
from core.logcontroller import log
from curd.authentication import user_scopes

token_router = APIRouter()

token_router = APIRouter(prefix="/authorization")


@token_router.post("/token", description="颁发用户token", name="用户授权")
async def SN_Authorization_Token(form_data: Annotated[OAuth2WithGroupRequest, Depends()]):
    log.debug(f"form_data: {form_data.__dict__}")
    """
    1. verify user's password
    2. verify user's permissions
    3. verify user's group
    """
    if form_data.username and form_data.password:
        user = await User.filter(username=form_data.username).first()
        if not user:
            HTTP_E401("Username invalid or password incorrect")
        # get user from database
        password_verify_result = await verify_password(form_data.password, user.password)
        # verify password
        if not password_verify_result:
            HTTP_E401("Username invalid or password incorrect")
        user_permissions = await get_user_permissions(user.user_id)
        request_scopes = form_data.scopes
        log.debug(f"User's permissions: {user_permissions}")
        log.debug(f"Request scopes:     {request_scopes}")
        # if request_scopes is subset of user_permissions
        if not set(request_scopes).issubset(set(user_permissions)):
            HTTP_E401("The scope obtained by the user exceeds the scope owned by the user, please try again")
        request_group = form_data.group_name
        jwt_data = {}
        # basic authorization passed
        jwt_data.update({
            "uid": user.user_id,
            "per": request_scopes,
        })
        
        if request_group:  
            group = await Group.filter(group_name=request_group).first()
            if not group:
                HTTP_E401("The group does not exist")
            group_user = await GroupUser.get(group_id=group.group_id,user_id=user.user_id)
            if not group_user:
                HTTP_E401("The user is not in the group")
            jwt_data.update({
                "gid": group.group_id,
            })
        
        token = create_access_token(jwt_data)
        return {"access_token": token, "token_type": "bearer"}

@token_router.get("/oauth/userscopes",
                  deprecated=True,)
async def SN_Authorization_UserScopes():
    return user_scopes
