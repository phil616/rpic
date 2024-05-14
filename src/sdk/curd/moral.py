import streamlit as st
from net import HTTP
def get_student_moral_record(username):
    r = HTTP.get(f"/api/v1/get/UserMoralRecord?username={username}")
    return r.json().get("data")
def get_moral_record_by_id(moral_record_id):
    r = HTTP.get(f"/api/v1/get/MoralRecord?moral_record_id={moral_record_id}")
    return r.json().get("data")
def get_all_unchecked_moral_record()->list:
    r = HTTP.get("/api/v1/get/uncheckedMoralRecord?status=1")
    return r.json().get("data")

def pass_moral_record(json):
    r = HTTP.json_post("/api/v1/update/checkMoralRecord",data=json)
    st.toast(r)
def unpass_moral_record(json):
    r = HTTP.json_post("/api/v1/update/checkMoralRecord",data=json)
    st.toast(r)
def display_moral_record_info(moral_records,username=None):
    """
    moral_records:
    [
        {
        "rec_id": 1,
        "action_id": 1,
        "action_score": 0,
        "rec_username": "test",
        "rec_urls": "string",
        "rec_msg": "acs",
        "rec_status": 1,
        "chk_username": "未审核，无审核人",
        "chk_commit": "None"
        }
    ]
    """
    for record in moral_records:
        with st.expander(f"{record['rec_username']}的德育分申请详情"):
            col1 ,col2= st.columns(2)
            with col1:
                st.write(f"ID: {record['rec_id']}")
                st.write(f"活动ID: {record['action_id']}")
                st.write(f"活动分值：{record['action_score']}")
                st.write(f"活动链接：{record['rec_urls']}")
                st.write(f"申请留言：{record['rec_msg']}")
                st.write(f"申请状态码：{record['rec_status']}")
                st.write(f"审核员：{record['chk_username']}")
                st.write(f"审核纪律：{record['chk_commit']}")
                comment = st.text_input(label="审核备注",value="")
                ck_user = st.text_input(label="审核人",value=st.session_state.username)
                pass_submit_data = {
                    "rec_id": record['rec_id'],
                    "rec_status": 2,
                    "chk_username": ck_user,
                    "chk_commit": comment
                }
                unpass_submit_data = {
                    "rec_id": record['rec_id'],
                    "rec_status": 3,
                    "chk_username": "ck_user",
                    "chk_commit": comment
                }
                st.form_submit_button(label="通过",on_click=pass_moral_record,args=(pass_submit_data,))
                st.form_submit_button(label="驳回",on_click=unpass_moral_record,args=(unpass_submit_data,))

def inline_moral_mode():
    HTTP.update_headers({"Authorization":"bearer "+st.session_state.token})
    st.header("德育分条目管理")

    with st.form(key='get_moral_record'):
        username = st.text_input("输入用户名")
        if st.form_submit_button(label='查询该学生所有德育分条目'):
            moral_record = get_student_moral_record(username)
            if moral_record:
                display_moral_record_info(moral_record,username)
    st.markdown("---")

    st.subheader("所有未审查的德育分条目")
    with st.form(key='check_unck_moral_record'):
        unchecklist = get_all_unchecked_moral_record()
        if unchecklist:
            display_moral_record_info(unchecklist)
