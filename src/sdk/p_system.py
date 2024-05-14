
import streamlit as st


def inline_pass():
    ...
def system_page():
    side_modules = [
        "主界面",
        "过程执行管理",
        "过程CURD管理",
        "用户管理",
        "用户组管理",
        "系统管理",
        "系统状态",
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
    elif option == "过程执行管理":
         ...
