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

import streamlit as st
from loguru import logger

from authencation import login,logout,prelogin

from p_admin import admin_page
from p_creator import creator_page
from p_system import system_page
from p_user import user_page

from conf import STR2TOLE

exec_wrapper = {
    "admin":admin_page,
    "user":user_page,
    "creater":creator_page,
    "system":system_page,
}

def main():
    st.session_state.authenticated = False
    prelogin()
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'token' not in st.session_state:
        st.session_state.token = ''
    if 'username' not in st.session_state:
        st.session_state.username = ''
    
    if not st.session_state.authenticated:
        login_container = st.container()
        with login_container:
            st.title("RPIC管理页面")
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
            role = st.radio("选择角色",tuple(list(STR2TOLE.keys())))
            with_group = st.text_input("组名称",help="默认system组名称为system_user_group")
            if st.button("登录"):
                login(username, password,role,with_group)
    else:
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            st.title("登陆成功")
            st.write(f"欢迎 {st.session_state.role} 用户 {st.session_state.uid}")
            st.write(f"当前用户组id为{st.session_state.group_id}")
        with col3:
            st.write("line 34")
        with col3:
            if st.button("退出登录"):
                logout()
        exec_wrapper[st.session_state.role]()



if __name__ == "__main__":
    main()