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