import streamlit as st
from net import HTTP
from typing import List,Union
from net import iso_format

def get_student_score_form(username)->Union[List,None]:
    resp = HTTP.get(f"/api/v1/gpa/get/user/scorelist?username={username}")
    return resp.json()  # list []
def add_student_score(username,gpa_type,gpa_score,gpa_time):
    resp = HTTP.json_post("/api/v1/gpa/new/user/score",{
        "username": username,
        "gpa_type": gpa_type,
        "gpa_score": gpa_score,
        "gpa_time": gpa_time
    })
    return resp.status_code == 200
def delete_student_score(gpa_id):
    resp = HTTP.get(f"/api/v1/gpa/delete/user/score?gid={gpa_id}")
    if resp.status_code == 200:
        return True
    else:
        return False
    
def update_student_score(gpa_id,username,gpa_type,gpa_score,gpa_time):
    resp = HTTP.json_post(f"/api/v1/gpa/update/user/score?gid={gpa_id}",{
        "username": username,
        "gpa_type": gpa_type,
        "gpa_score": gpa_score,
        "gpa_time": gpa_time
        })
    if resp.status_code == 200:
        return True
    else:
        return False
def display_student_score_info(score_info,username):
    """
    score_info excepted form:
    [
    {
        "gpa_score": "92",
        "gpa_time": "2023-1",
        "update_by": "系统修改",
        "gpa_type": "线性代数",
        "gpa_id": 1,
        "create_time": "2024-04-09T23:32:14.850815+08:00",
        "update_time": "2024-04-09T23:32:14.850815+08:00",
        "username": "test",
        "create_by": "系统创建"
    },
    """
    st.write(f"用户名：{username} 的成绩如下")
    for score in score_info:
        with st.expander(f"{score['gpa_type']}的成绩详情"):
            col1 ,col2= st.columns(2)
            with col1:
                st.write(f"用户名：{username}")
                st.write(f"成绩：{score['gpa_score']}")
                st.write(f"时间：{score['gpa_time']}")
                st.write(f"创建时间：{iso_format(score['create_time'])}")
                st.write(f"更新时间：{iso_format(score['update_time'])}")
                st.write(f"创建人：{score['create_by']}")
                st.write(f"更新人：{score['update_by']}")
                st.write(f"id：{score['gpa_id']}")
    st.markdown("---")



def inline_score():
    HTTP.update_headers({"Authorization":"bearer "+st.session_state.token})
    st.header("成绩分数管理")

   # 获取学生信息
    st.subheader("查询学生所有成绩")
    
    with st.form(key='get_score_form'):
        username = st.text_input("输入用户名")
        if st.form_submit_button(label='查询该学生所有成绩'):
            student_info = get_student_score_form(username)
            if student_info:
                display_student_score_info(student_info,username)

    st.markdown("---")
    st.subheader("添加学生成绩")

    with st.form(key='add_score_form'):
        """{
        "username": "string",
        "gpa_type": "string",
        "gpa_score": "string",
        "gpa_time": "string"
        }"""
        username = st.text_input("输入用户名")
        gpa_type = st.text_input("输入课程名称")
        gpa_score = st.number_input("输入成绩")
        gpa_time = st.date_input("输入时间")
        if st.form_submit_button(label='添加学生成绩'):
            if add_student_score(username,gpa_type,str(gpa_score),str(gpa_time.isoformat())):
                st.success("添加成功")
            else:
                st.error("添加失败")

    st.markdown("---")
    st.subheader("修改学生成绩")
    with st.form(key='update_score_form'):
        """{
        "username": "string",
        "gpa_type": "string",
        "gpa_score": "string",
        "gpa_time": "string"
        }"""
        gid = st.number_input("输入成绩ID",max_value=1,step=1)
        username = st.text_input("输入用户名")
        gpa_type = st.text_input("输入课程名称")
        gpa_score = st.number_input("输入成绩")
        gpa_time = st.date_input("输入时间")
        if st.form_submit_button(label='修改学生成绩'):
            if update_student_score(gid,username,gpa_type,str(gpa_score),str(gpa_time.isoformat())):
                st.success("修改成功")
            else:
                st.error("修改失败")

    st.markdown("---")  
    st.subheader("删除学生某项成绩")
    gid = st.number_input("输入成绩ID",min_value=1,step=1)
    if st.button("删除"):
        if delete_student_score(gid):
            st.success("删除成功")
        else:
            st.error("删除失败")

    
            