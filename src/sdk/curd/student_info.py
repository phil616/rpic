import streamlit as st
from net import HTTP
def get_student_info(username):
    response = HTTP.get(f"/api/v1/get/studentInfo?username={username}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("获取学生信息失败")
        return None

def display_student_info(student_info):
    with st.expander(f"查询成功：点击展开学生详细信息: {student_info['stu_name']} - {student_info['stu_id']}"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**用户名:** {student_info['username']}")
            st.write(f"**学号:** {student_info['stu_id']}")
            st.write(f"**姓名:** {student_info['stu_name']}")
            st.write(f"**班级:** {student_info['stu_clazz']}")
            st.write(f"**性别:** {student_info['stu_sex']}")
            st.write(f"**身份证号:** {student_info['stu_card']}")
            st.write(f"**民族:** {student_info['stu_nation']}")
            st.write(f"**政治面貌:** {student_info['stu_politics']}")
        with col2:
            st.write(f"**籍贯:** {student_info['stu_origin']}")
            st.write(f"**家庭住址:** {student_info['stu_home']}")
            st.write(f"**手机号:** {student_info['stu_phone']}")
            st.write(f"**邮箱:** {student_info['stu_email']}")
            st.write(f"**现住址:** {student_info['stu_location']}")
            st.write(f"**学籍状态:** {student_info['stu_status']}")
            st.write(f"**毕业去向:** {student_info['stu_graduate']}")

def create_student_info(student_info):
    response = HTTP.json_post("/api/v1/post/studentInfo", json=student_info)
    if response.status_code == 200:
        st.success("学生信息创建成功")
    else:
        st.error("学生信息创建失败")

def update_student_info(student_info):
    response = HTTP.json_post("/api/v1/update/studentInfo", json=student_info)
    if response.status_code == 200:
        st.success("学生信息更新成功")
    else:
        st.error("学生信息更新失败")

def delete_student_info(username):
    response = HTTP.get(f"/api/v1/post/studentInfo?username={username}")
    if response.status_code == 200:
        st.success("学生信息删除成功")
    else:
        st.error("学生信息删除失败")

def inline_student_curd():
    HTTP.update_headers({"Authorization":"bearer "+st.session_state.token})
    st.header("学生信息管理")

   # 获取学生信息
    st.subheader("获取学生信息")
    with st.form(key='get_student_info_form'):
        username = st.text_input("用户名")
        if st.form_submit_button(label='获取'):
            student_info = get_student_info(username)
            if student_info:
                display_student_info(student_info)

    # 创建学生信息
    st.subheader("创建学生信息")
    with st.form(key='create_student_info_form'):
        """
        {
          "username": "string",
          "stu_id": "string",
          "stu_name": "string",
          "stu_clazz": "string",
          "stu_sex": "string",
          "stu_card": "string",
          "stu_nation": "string", 
          "stu_politics": "string",
          "stu_origin": "string",
          "stu_home": "string",
          "stu_phone": "string",
          "stu_email": "string",
          "stu_location": "string",
          "stu_status": "string",
          "stu_graduate": "string"
        }
        """
        username = st.text_input("用户名")
        stu_id = st.text_input("学号")
        stu_name = st.text_input("姓名")
        stu_clazz = st.text_input("班级")
        stu_sex = st.text_input("性别")
        stu_card = st.text_input("身份证号")
        stu_nation = st.text_input("民族")
        stu_politics = st.text_input("政治面貌")
        stu_origin = st.text_input("籍贯")
        stu_home = st.text_input("家庭住址")
        stu_phone = st.text_input("手机号")
        stu_email = st.text_input("邮箱")
        stu_location = st.text_input("现住址")
        stu_status = st.text_input("学籍状态")
        stu_graduate = st.text_input("毕业去向")
        
        if st.form_submit_button(label='创建'):
            student_info = {
                "username": username,
                "stu_id": stu_id,
                "stu_name": stu_name,
                "stu_clazz": stu_clazz,
                "stu_sex": stu_sex,
                "stu_card": stu_card,
                "stu_nation": stu_nation,
                "stu_politics": stu_politics,
                "stu_origin": stu_origin, 
                "stu_home": stu_home,
                "stu_phone": stu_phone,
                "stu_email": stu_email,
                "stu_location": stu_location,
                "stu_status": stu_status,
                "stu_graduate": stu_graduate
            }
            create_student_info(student_info)

    # 更新学生信息        
    st.subheader("更新学生信息")
    with st.form(key='update_student_info_form'):
        username = st.text_input("用户名")
        stu_id = st.text_input("学号")
        stu_name = st.text_input("姓名")
        stu_clazz = st.text_input("班级")
        stu_sex = st.text_input("性别")
        stu_card = st.text_input("身份证号")
        stu_nation = st.text_input("民族")
        stu_politics = st.text_input("政治面貌")
        stu_origin = st.text_input("籍贯")
        stu_home = st.text_input("家庭住址")
        stu_phone = st.text_input("手机号")
        stu_email = st.text_input("邮箱")
        stu_location = st.text_input("现住址")
        stu_status = st.text_input("学籍状态") 
        stu_graduate = st.text_input("毕业去向")
        
        if st.form_submit_button(label='更新'):
            student_info = {
                "username": username,
                "stu_id": stu_id,
                "stu_name": stu_name,
                "stu_clazz": stu_clazz,
                "stu_sex": stu_sex,
                "stu_card": stu_card,
                "stu_nation": stu_nation,
                "stu_politics": stu_politics,
                "stu_origin": stu_origin,
                "stu_home": stu_home,
                "stu_phone": stu_phone,
                "stu_email": stu_email,
                "stu_location": stu_location,
                "stu_status": stu_status,
                "stu_graduate": stu_graduate
            }
            update_student_info(student_info)
            
    # 删除学生信息
    st.subheader("删除学生信息")        
    with st.form(key='delete_student_info_form'):
        username = st.text_input("用户名")
        if st.form_submit_button(label='删除'):
            delete_student_info(username)

    st.write("这里是学生信息管理页面")