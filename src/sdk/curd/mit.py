import streamlit as st
from net import HTTP,reverse
from loguru import logger
mit_chioce = {"空状态":0,"参加保险":1,"放弃参加医保":2}
reverse_mit_chioce = reverse(mit_chioce)
def get_mit_status_mapping():
    response = HTTP.get("/api/v1/get/mit/static/mapping")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("获取医保状态码映射表失败")
        return None

def get_user_mit_status(username):
    response = HTTP.get(f"/api/v1/get/mit/userStatus?username={username}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("获取用户医保状态失败")
        return None

def create_mit_record(mit_data):
    logger.debug(mit_data)
    response = HTTP.json_post("/api/v1/crete/mit", data=mit_data)
    if response.status_code == 200:
        st.success("新建医保记录成功")
    else:
        st.error("新建医保记录失败,检查用户名或是否重复录入")

def display_mit_status(mit_status, status_mapping):
    """
    {
        "id": 1,
        "username": "test",
        "mit_status": 0,
        "mit_attachments": "null",
        "mit_info": "{'comment': 'ac'}",
        "mit_choice": 0,
        "mit_on": true,
        "mit_msgmap": "空状态"
        }
    """
    with st.expander(f"查询成功：点击展开学生详细信息: {mit_status['id']} - {mit_status['username']}"):
        col1, col2 = st.columns(2)
        logger.debug(mit_status['mit_status'])
        r = status_mapping.get(str(mit_status['mit_status']))
        logger.debug(status_mapping)
        with col1:
            st.write(f"**用户名:** {mit_status['username']}")
            st.write(f"**ID:** {mit_status['id']}")
            st.write(f"**参保状态:** {r}")
            st.write(f"**参保信息:** {mit_status['mit_info']}")
            sst =  reverse_mit_chioce[mit_status["mit_choice"]]
            st.write(f"**参保情况:** {sst}")
            st.write(f"**是否在保:** {mit_status['mit_msgmap']}")


def display_status_mapping(status_mapping):
    st.subheader("医保状态码映射表")
    table_data = [
        {"状态码": code, "描述": description}
        for code, description in status_mapping.get("data").items()
    ]
    st.table(table_data)
def in_line_mit():
    st.title("学生医保事务")

    status_mapping = get_mit_status_mapping()
    display_status_mapping(status_mapping)
    st.subheader("查询用户医保状态")
    username = st.text_input("输入用户名")
    if st.button("查询"):
        mit_status = get_user_mit_status(username)
        if mit_status:
            display_mit_status(mit_status, status_mapping["data"])

    st.subheader("新建医保记录")

    with st.form(key='create_mit_form'):
        username = st.text_input("用户名")
        status = st.selectbox("医保状态", options=list(status_mapping.get("data").values()))
        mit_status_mapping = reverse(status_mapping.get("data"))
        mit_number = st.selectbox("医保状态", options=list(mit_chioce.keys()))
        remark = st.text_area("备注")

        if st.form_submit_button("提交"):
            status_code = mit_status_mapping.get(status)
            mit_number_code = mit_chioce[mit_number]

            mit_data = {
                "username": username,
                "mit_status": int(status_code),
                "mit_number": int(mit_number_code),
                "mit_info": str({"comment":remark}),
                "mit_attachments":"null",
                "mit_on":"true",
                "mit_msgmap":str(status)
            }
            create_mit_record(mit_data)