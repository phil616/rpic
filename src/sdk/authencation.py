import streamlit as st
import conf
import jwt
from net import HTTP,OAuth_group_dict
from loguru import logger
def parse_jwt(token:str)->dict:
    try:
        payload = jwt.decode(token,algorithms=["HS256"],options={"verify_signature": False})
        logger.debug(f"JWT has been parsed, {payload}")
    except Exception as e:
        logger.error(e)
    return payload

def logout():
    with open(conf.TOKEN_FILE, "w") as file:
        file.write("")
    st.session_state.authenticated = False
    st.session_state.token = ''
    st.session_state.username = ''
    st.experimental_rerun()

def save_token(token):
    with open(conf.TOKEN_FILE, "w") as file:
        file.write(token)

def load_token():
    try:
        with open(conf.TOKEN_FILE, "r") as file:
            data =file.read().strip()
            return data
    except FileNotFoundError:
        return None

def login(username:str, password:str,role:str,with_group):
    st.session_state.role = conf.STR2TOLE[role]
    scopes = conf.ROLE2SCOPE[conf.STR2TOLE[role]]
    logger.debug(f"except_scope = {scopes}")
    try:
        OAuth_group_dict.update({"username":username,"password":password,"group_name":with_group,"scope":scopes})
        # send post to api
        response = HTTP.data_post("/authorization/token", data=OAuth_group_dict)
        if response.status_code == 200:
            token = response.json()["access_token"]
            save_token(token) 
            logger.info(f"login success, get token {token[0:16]}")
            st.session_state.authenticated = True
            st.session_state.token = token
            st.session_state.username = parse_jwt(token).get("usr")
            st.session_state.uid = parse_jwt(token).get("uid")
            st.session_state.scopes = parse_jwt(token).get("per")
            st.session_state.role = conf.STR2TOLE[role]  # admin, user, creator, system
            st.session_state.group_id = parse_jwt(token).get("gid")
            st.rerun()
        else:
            st.session_state.authenticated = False
            st.error("无效的用户名或密码")
    except Exception as e:
        logger.error(e)
        st.error("登录请求失败,请检查API是否正常工作")

def prelogin():
    token = load_token()
    if token:
        HTTP.update_headers({"Authorization":"Bearer "+token})
        resp = HTTP.get("/user/get/info")
        if resp.status_code == 200:
            st.session_state.role = resp.json().get("user_roles")[0]
        logger.debug("prelogin activated token vaild, token has been cached")
        """
        Examples:
        JWT has been parsed, 
        {'uid': 4, 'per': ['PROCEDURE:ACCESS', 'PROCEDURE:MODIFY', 'PROCEDURE:ADMIN', 'GROUP:CURD', 'GROUP:ENDPOINT', 'USER:CURD', 'SYSTEM:HARDWARE'], 
        'gid': 1, 'exp': 1715750593, 'iss': 'RPICS Backend'}
        """
        st.session_state.authenticated = True
        st.session_state.token = token
        st.session_state.username = parse_jwt(token).get("usr")
        st.session_state.uid = parse_jwt(token).get("uid")
        st.session_state.scopes = parse_jwt(token).get("per")
        #ROLE IS NOT IN USE st.session_state.role = conf.STR2TOLE[role]  # admin, user, creator, system
        st.session_state.group_id = parse_jwt(token).get("gid")
    else:
        st.session_state.authenticated = False 