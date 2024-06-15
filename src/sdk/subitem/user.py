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

from pydantic import BaseModel
from net import HTTP
import streamlit as st
import pandas as pd
from typing import List, Any,Dict
class UserBasicSchema(BaseModel):
    username: str
    password: str
    user_info: dict
    user_roles: str
    user_status: int

# CURD user

def get_all_users():
    resp = HTTP.get("/user/all")
    return resp.json()

def get_current_user_info() -> Dict:
    """ EXAMPLE:
    {
    "user_basic": {
        "uid": 4,
        "username": "system",
        "status": 1
    },
    "user_info": {},
    "user_roles": [
        "system"
    ],
    "permissions": [
        "PROCEDURE:ACCESS",
        "PROCEDURE:MODIFY",
        "PROCEDURE:ADMIN",
        "GROUP:CURD",
        "GROUP:ENDPOINT",
        "USER:CURD",
        "SYSTEM:HARDWARE"
    ],
    "groups": [
        {
        "update_time": "2024-05-14T04:37:36.951881+08:00",
        "create_by": "[system]",
        "create_time": "2024-05-14T04:37:36.951881+08:00",
        "id": 1,
        "update_by": "[system]",
        "user_id": 4,
        "group_id": 1
        }
    ],
    "group_admins": [
        {
        "update_time": "2024-05-14T04:37:22.427344+08:00",
        "group_status": 1,
        "group_name": "system_user_group",
        "create_by": "[system]",
        "create_time": "2024-05-14T04:37:22.427344+08:00",
        "update_by": "[system]",
        "group_administrator": 4,
        "group_info": {},
        "group_id": 1
        }
    ]
    }
    """
    resp = HTTP.get("/user/get/info")
    return resp.json()
    

def create_user(user:UserBasicSchema):
    resp = HTTP.json_post("/user/create", user.model_dump_json())
    return resp.json()
    ...
def delete_user():
    ...
    # not going to impl
def update_user():
    ...
    # not going to impl
def inline_user():
    st.header("User")
    st.subheader("Get all users")
    user_json_format = get_all_users()
    pd_table = pd.DataFrame(user_json_format)
    st.write(pd_table)
    st.subheader("Get current user info")
    user_info = get_current_user_info()
    st.write(user_info)
    st.subheader("Create user")
    add_user_container = st.container()
    with add_user_container:
        new_username = st.text_input(label="Username")
        new_password = st.text_input(label="Password")
        new_user_roles = st.text_input(label="User roles",value="user")
        new_user_info = st.text_input(label="User info",value="")
        new_user_status = st.number_input(label="User status",value=1)
        userSchema = UserBasicSchema(
            username=new_username,
            password=new_password,
            user_info={"msg":new_user_info},
            user_roles=new_user_roles,
            user_status=new_user_status
        )
        if st.button("Create user"):
            create_user(userSchema)
            # TODO: add delete and update
