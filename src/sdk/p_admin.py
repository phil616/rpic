
import streamlit as st

from curd.users import inline_user_curd
def inline_pass():
    ...
def admin_page():
    st.sidebar.title("管理员功能")
    side_modules = [
        "主界面",
        "用户管理",
        "德育分活动管理",
        "德育分管理",
        "学生档案管理",
        "学生医保管理",
        "学生材料管理",
        "学生成绩管理",
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

    elif option == "用户管理":
        inline_user_curd()
    elif option == "德育分活动管理":
        inline_pass()
    elif option == "德育分管理":
        inline_pass()
    elif option == "学生档案管理":
        ...
    elif option == "学生医保管理":
        ...
    elif option == "学生材料管理":
        ...
    elif option == "学生成绩管理":
        ...
