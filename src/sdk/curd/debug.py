import streamlit as st
from net import HTTP
from loguru import logger
def check_url_status(url):
    try:
        response = HTTP.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        logger.debug(e)
        return False

def inline_debug():


    st.title("URL 状态检查器")

    urls = {
        "系统连通测试": "/api/v1/get/basic/info",
        "权限测试": "/api/v1/group",
        "状态测试": "/api/v1/normal",
    }

    for name, url in urls.items():
        container = st.container()
        cols = container.columns(2)

        with cols[0]:
            st.write(f"## {name}")
            button_clicked = st.button(f"检查 {name}", key=f"button_{name}")

        with cols[1]:
            if button_clicked:
                status = check_url_status(url)
                if status:
                    st.success(f"{name} 可达 :white_check_mark:")
                else:
                    st.error(f"{name} 不可达 :x:")
