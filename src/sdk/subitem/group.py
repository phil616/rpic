
# CURD USER GROUP
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

def get_all_groups():
    resp = HTTP.get("/group/get/all")
    
# Relate USER GROUP
def inline_group():
    pass