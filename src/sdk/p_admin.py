
import streamlit as st
from subitem.user import inline_user
from subitem.curd_procedure import inline_curd_procedure
def inline_pass():
    ...
def admin_page():
    side_modules = [
        "主界面",
        "过程执行管理",
        "过程CURD管理",
        "用户管理",
        "用户组管理",
        "用户状态",
    ]
    option = st.sidebar.radio("导航", tuple(side_modules))
    if option == "主界面":
            # 标题 + 介绍
            st.title("后台管理系统")
            st.markdown("""
                        ## 介绍
                        这是一个后台管理系统，用于管理学生信息。
                        ## 开发人员
                        - 张三
            """)
    elif option == "过程执行管理":  # e-procedure
         ...
    elif option == "过程CURD管理":  # curd_pro
         inline_curd_procedure()
    elif option == "用户管理":  # user
        inline_user()
    elif option == "用户组管理":  # group
         ...
    elif option == "用户状态":  # ....
        ...