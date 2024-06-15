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


def inline_pass():
    ...
def creator_page():
    side_modules = [
        "主界面",
        "过程执行管理",
        "过程CURD管理",
        "用户状态",
    ]
    option = st.sidebar.radio("导航", tuple(side_modules))
    if option == "主界面":
            # 标题 + 介绍
            st.title("后台管理系统")
            st.markdown("""
                        ## 介绍
                        这是一个后台管理系统，用于模拟开发者的行为
                        ## 开发人员
                        - 费东旭
            """)
    elif option == "过程执行管理":  # e-procedure
         ...
    elif option == "过程CURD管理":  # curd_pro
         ...
    elif option == "用户状态":  # user
        ...
