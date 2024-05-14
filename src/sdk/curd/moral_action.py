import streamlit as st
from net import HTTP
from datetime import datetime, time, timezone


def format_datetime(iso_datetime):
    # 将 ISO 格式的日期时间字符串转换为 datetime 对象
    dt = datetime.fromisoformat(iso_datetime.replace('Z', '+00:00'))
    
    # 使用字符串格式化将 datetime 对象转换为指定格式的字符串
    formatted_datetime = dt.strftime("%Y年%m月%d日%H时%M分%S秒")
    
    return formatted_datetime


def get_all_moral_action():
    """获取所有的德育分活动，包括不可用"""
    response = HTTP.get("/api/v1/get/AllMoralActio")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("获取学生信息失败")
        return None
def get_all_available_moral_action():
    """获取可用的德育分活动"""
    response = HTTP.get("/api/v1/get/MoralAction")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("获取学生信息失败")
        return None
    
def display_moral_action_info(moral_action_info):
    moral_action_infos = moral_action_info.get("data")
    """
    resp:
    {
    "data": [
        {
        "action_id": 1,
        "action_on": true,
        "action_grant": "系统创建",
        "action_reduce": false,
        "action_date": "2024-04-10T11:34:01.270438+08:00",
        "action_score": 0,
        "action_title": "string",
        "action_type": 0,
        "action_detail": "string"
        }
    ]
    }
    """
    for moral_action_info in moral_action_infos:
        with st.expander(f"查询成功！点击展开活动详细信息: {moral_action_info['action_id']} - {moral_action_info['action_title']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**ID:** {moral_action_info['action_id']}")
                st.write(f"**活动名称:** {moral_action_info['action_title']}")
                st.write(f"**活动类型:** {moral_action_info['action_type']}")
                # 时间转为正常时间格式
                action_date = format_datetime(moral_action_info['action_date'])
                st.write(f"**活动时间:** {action_date}")
                st.write(f"**活动详情:** {moral_action_info['action_detail']}")
                st.write(f"**活动分数:** {moral_action_info['action_score']}")
                # 活动状态转为正常状态
                if moral_action_info['action_on']:
                    st.write("**活动状态:** 可用")
                else:
                    st.write("**活动状态:** 不可用")
                st.write(f"**活动创建人:** {moral_action_info['action_grant']}")
                st.write(f"**活动是否扣分:** {moral_action_info['action_reduce']}")
                # 创建时间转为正常时间格式
                action_date = format_datetime(moral_action_info['action_date'])
                st.write(f"**活动创建时间:** {action_date}")


def create_moral_action(moral_action_info):
    """except data form:
    {
        "action_on": true,
        "action_grant": "系统创建",
        "action_reduce": false,
        "action_date": "2024-04-10T03:33:09.523Z",
        "action_score": 0,
        "action_title": "string",
        "action_type": 0,
        "action_detail": "string"
    }
    """
    response = HTTP.json_post("/api/v1/add/MoralAction", data=moral_action_info)
    if response.status_code == 200:
        st.success("学生信息创建成功")
    else:
        st.error("学生信息创建失败")

def update_moral_action_info(moral_action_info,moral_action_id):
    response = HTTP.json_post(f"/api/v1/update/MoralAction?action_id={moral_action_id}", data=moral_action_info)
    if response.status_code == 200:
        st.success("学生信息更新成功")
    else:
        st.error("学生信息更新失败")
    

def delete_moral_action_info(action_id):
    response = HTTP.get(f"/api/v1/delete/MoralAction?action_id={action_id}")
    if response.status_code == 200:
        st.success("学生信息删除成功")
    else:
        st.error("学生信息删除失败")

def inline_moral_action():
    HTTP.update_headers({"Authorization":"bearer "+st.session_state.token})
    st.header("德育分活动管理")

   # 获取学生信息
    st.subheader("获取所有活动")
    with st.form(key='get_moral_action_form'):
        if st.form_submit_button(label='获取所有可用德育分活动'):
            student_info = get_all_available_moral_action()
            if student_info:
                display_moral_action_info(student_info)
        """
        if st.form_submit_button(label='获取所有德育分活动（包含不可用活动）'):
            student_info = get_all_moral_action()
            if student_info:
                display_moral_action_info(student_info)
        """
    # 创建学生信息
    st.subheader("创建德育分活动")
    with st.form(key='create_moral_action_form'):
        """
        {
            "action_on": true,
            "action_grant": "系统创建",
            "action_reduce": false,
            "action_date": "2024-04-10T03:33:53.529Z",
            "action_score": 0,
            "action_title": "string",
            "action_type": 0,
            "action_detail": "string"
        }
        """
        action_title = st.text_input("活动标题")
        action_detail = st.text_input("活动详情")
        action_on= st.selectbox(label="是否立即启用",options=["是","否"])
        if action_on == "是":
            action_on_data = True
        else:
            action_on_data = False
        action_grant = st.text_input("授权人",value="学院团委")
        action_reduce = st.selectbox(label="是否为扣分活动",options=["扣分","加分"])
        if action_reduce == "扣分":
            action_reduce_data = True
        else:
            action_reduce_data = False
          # 获取用户输入的日期
        input_date = st.date_input("请选择日期")

        # 获取用户输入的时间
        input_time = st.time_input("请选择时间", value=time(0, 0))

        if input_date and input_time:
            # 将日期和时间组合成一个 datetime 对象
            input_datetime = datetime.combine(input_date, input_time)

            # 将 datetime 对象转换为 ISO 格式的字符串
            iso_datetime = input_datetime.replace(tzinfo=timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

            st.success(f"转换后的 ISO 格式时间: {iso_datetime}")
        action_date = iso_datetime
        action_score = st.number_input(label="活动分值",min_value=0.1,step=0.1)

        if st.form_submit_button(label='创建'):
            student_info = {
            "action_on": action_on_data,
            "action_grant": action_grant,
            "action_reduce": action_reduce_data,
            "action_date": action_date,
            "action_score": action_score,
            "action_title": action_title,
            "action_type": 0,
            "action_detail": action_detail
            }
            create_moral_action(student_info)

    """
     更新德育分活动信息
    """    
    st.subheader("更新德育分活动信息")
    with st.form(key='update_moral_action_info_form'):
        """
        {
            "action_on": true,
            "action_grant": "系统创建",
            "action_reduce": false,
            "action_date": "2024-04-10T03:33:53.529Z",
            "action_score": 0,
            "action_title": "string",
            "action_type": 0,
            "action_detail": "string"
        }
        """
        action_id = st.text_input("活动ID")
        action_title = st.text_input("活动标题")
        action_detail = st.text_input("活动详情")
        action_on= st.selectbox(label="是否立即启用",options=["是","否"])
        if action_on == "是":
            action_on_data = True
        else:
            action_on_data = False
        action_grant = st.text_input("授权人",value="学院团委")
        action_reduce = st.selectbox(label="是否为扣分活动",options=["扣分","加分"])
        if action_reduce == "扣分":
            action_reduce_data = True
        else:
            action_reduce_data = False
          # 获取用户输入的日期
        input_date = st.date_input("请选择日期")

        # 获取用户输入的时间
        input_time = st.time_input("请选择时间", value=time(0, 0))

        if input_date and input_time:
            # 将日期和时间组合成一个 datetime 对象
            input_datetime = datetime.combine(input_date, input_time)

            # 将 datetime 对象转换为 ISO 格式的字符串
            iso_datetime = input_datetime.replace(tzinfo=timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

            st.success(f"转换后的 ISO 格式时间: {iso_datetime}")
        action_date = iso_datetime
        action_score = st.number_input(label="活动分值",min_value=0.1,step=0.1)

        if st.form_submit_button(label='创建'):
            student_info = {
            "action_on": action_on_data,
            "action_grant": action_grant,
            "action_reduce": action_reduce_data,
            "action_date": action_date,
            "action_score": action_score,
            "action_title": action_title,
            "action_type": 0,
            "action_detail": action_detail
            }
            update_moral_action_info(student_info,int(action_id))
            
    # 删除学生信息
    st.subheader("删除德育分活动信息")        
    with st.form(key='delete_moral_action_info_form'):
        username = st.text_input("活动ID")
        if st.form_submit_button(label='删除'):
            delete_moral_action_info(username)

    st.write("这里是德育分管理页面")