import streamlit as st
from net import HTTP

def create_task(task_json):
    """excepted data
    {
        "act_grant": "string",
        "act_title": "string",
        "act_desc": "string",
        "act_range": "全体",
        "act_on": true
    }
    """
    r = HTTP.json_post("/api/v1/post/ImageTaskAction",data=task_json)
    st.toast(r.text)
    return r.json()

def inline_task_submit():
    HTTP.update_headers({"Authorization":"bearer "+st.session_state.token})
    with st.form(key="inline_task_form"):
        if st.form_submit_button("查询所有任务"):
            for item in HTTP.get("/api/v1/get/ImageActions").json():
                with st.expander(item["act_title"]):
                    col1 ,col2= st.columns(2)
                    with col1:
                        st.write(f"活动ID: {item['act_id']}")
                        st.write(f"活动授权人: {item['act_grant']}")
                        st.write(f"活动范围: {item['act_range']}")
                        st.write(f"活动状态: {item['act_on']}")
                        st.write(f"活动描述: {item['act_desc']}")


    st.header("材料任务管理")
    with st.form(key="create_task_form"):
        act_grant = st.text_input("授权人",value=st.session_state.username)
        act_title = st.text_input("任务标题")
        act_desc = st.text_input("任务描述")
        act_range = st.selectbox("任务范围",["全体","部门","个人"])
        act_on = st.checkbox("是否开启")
        if st.form_submit_button("提交"):
            create_task({
                "act_grant": act_grant,
                "act_title": act_title,
                "act_desc": act_desc,
                "act_range": act_range,
                "act_on": act_on
            })
    st.subheader("获取某个学生任务的完成情况")
    with st.form(key="get_task_form_user_id"):
        act_id = st.number_input("活动ID",value=1,step=1)
        username = st.number_input("用户名",value=1,step=1)
        if st.form_submit_button("查询"):
            r = HTTP.get(f"/api/v1/get/userImageRecord?act_id={act_id}&username={username}")
            st.write(r.json())