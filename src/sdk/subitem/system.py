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

from net import HTTP
import streamlit as st


def get_subapps():
    return HTTP.get("/mounting/subapp").json()

def mount_subapp():
    return HTTP.json_post("/mounting/mount",{
    "path":"test",
    "methods":"POST",
    "procedure_id":1
    }).json()
def inline_system():
    if st.button("获取节点"):
        st.write(get_subapps())

    if st.button("绑定节点"):
        st.write(mount_subapp())