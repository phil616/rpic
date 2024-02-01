from typing import Annotated
from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm
from core.authorize import OAuth2WithGroupRequest, create_access_token
from core.exceptions import HTTP_E401
from curd.authentication import verify_password, verify_user_password,get_user_permissions
from models.User import User
from models.GroupUser import GroupUser
from models.Group import Group

token_router = APIRouter()


token_router = APIRouter(prefix="/authorization")


@token_router.post("/token", description="颁发用户token", name="用户授权")
async def SN_Authorization_Token(form_data: Annotated[OAuth2WithGroupRequest, Depends()]):
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
        if request_scopes not in user_permissions:
            HTTP_E401("The scope obtained by the user exceeds the scope owned by the user, please try again")
        request_group = form_data.group_name
        jwt_data = {}
        # basic authorization passed
        jwt_data.update({
            "uid": user.user_id,
            "per": request_scopes,
        })
        
        if request_group:  
            group = await Group.get(group_name=request_group)
            group_user = await GroupUser.get(group_id=group.group_id,user_id=user.user_id)
            if not group_user:
                HTTP_E401("The user is not in the group")
            jwt_data.update({
                "gid": group.group_id,
            })
        
        token = create_access_token(jwt_data)
        return {"access_token": token, "token_type": "bearer"}

