import streamlit as st
import requests
from net import HTTP
from conf import BASEURL as API_URL
"""
CURD user model:
{
  "username": "string",
  "password": "string",
  "user_scope": 0,
  "user_clazz": "string",
  "user_phone": "string",
  "user_info": {}
}
openapi:
 "/api/v1/get/users": {
            "get": {
                "tags": [
                    "资源管理"
                ],
                "summary": "Mf Get All Users",
                "operationId": "MF_GET_ALL_USERS_api_v1_get_users_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                }
            }
        },
        "/api/v1/delete/user": {
            "get": {
                "tags": [
                    "资源管理"
                ],
                "summary": "Mf Delete User By User Id",
                "operationId": "MF_delete_user_by_user_id_api_v1_delete_user_get",
                "parameters": [
                    {
                        "name": "userid",
                        "in": "query",
                        "required": true,
                        "schema": {
                            "type": "integer",
                            "title": "Userid"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/v1/create/user": {
            "post": {
                "tags": [
                    "资源管理"
                ],
                "summary": "Mf New User",
                "operationId": "MF_new_user_api_v1_create_user_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/UserSchema"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/StdResp"
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/v1/update/user": {
            "post": {
                "tags": [
                    "资源管理"
                ],
                "summary": "Mf Update User",
                "operationId": "MF_update_user_api_v1_update_user_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/UserSchema"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/StdResp"
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
"""
def get_users():
    response = HTTP.get("/api/v1/get/users")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("获取学生数据失败")
        return []

def add_user(user):
    response = HTTP.json_post("/api/v1/create/user", json=user)
    if response.status_code == 200:
        st.success("学生添加成功")
    else:
        st.error("学生添加失败")

def update_user(updated_student):
    response = HTTP.json_post("/api/v1/update/user", json=updated_student)
    if response.status_code == 200:
        st.success("学生信息更新成功")
    else:
        st.error("学生信息更新失败")

def delete_user(student_id):
    response = requests.delete(f"{API_URL}/api/v1/delete/user/?user_id={student_id}")
    if response.status_code == 204:
        st.success("学生删除成功")
    else:
        st.error("学生删除失败")
def inline_user_curd():
    st.header("学生信息管理")
    users = get_users()
    if users:
        for user in users:
            # exclude field: password,update_time
            user.pop("password")
            user.pop("update_time")
        st.write("\n使用 st.table() 展示用户信息:")
        st.table(users)
        # 添加学生
    st.subheader("添加学生")
    with st.form(key='add_student_form'):
        username = st.text_input("用户名")
        password = st.text_input("密码")
        user_scope = st.number_input("用户权限", min_value=0, max_value=15, step=1)
        user_clazz = st.text_input("班级")
        user_phone = st.text_input("手机号")
        user_info = st.text_input("用户信息")

        if st.form_submit_button(label='添加'):
            user = {"username": username, "password": password, "user_scope": user_scope, "user_clazz": user_clazz, "user_phone": user_phone, "user_info": user_info}
            add_user(user)
        
    # 更新用户信息
    st.subheader("更新用户信息")
    with st.form(key='update_user_form'):
        """
        {
            "username": "string",
            "password": "string",
            "user_scope": 0,
            "user_clazz": "string",
            "user_phone": "string",
            "user_info": {}
        }
        """
        username = st.text_input("用户名")
        password = st.text_input("密码")
        user_scope = st.number_input("用户权限", min_value=0, max_value=15, step=1)
        user_clazz = st.text_input("班级")
        user_phone = st.text_input("手机号")
        user_info = st.text_input("用户信息")

        if st.form_submit_button(label='更新'):
            updated_user = {"username": username, "password": password, "user_scope": user_scope, "user_clazz": user_clazz, "user_phone": user_phone, "user_info": user_info}
            update_user(updated_user)
        
        
    # 删除学生
    st.subheader("删除用户")
    with st.form(key='delete_student_form'):
        user_id = st.number_input("用户ID", min_value=1, step=1)
        if st.form_submit_button(label='删除'):
            delete_user(user_id)
    st.write("这里是学生信息管理页面")


"""
CURD Student Model
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
openapi:
"/api/v1/get/studentInfo": {
            "get": {
                "tags": [
                    "学生信息事务"
                ],
                "summary": "获取学生信息",
                "description": "通过token获取学生信息",
                "operationId": "获取学生信息_api_v1_get_studentInfo_get",
                "security": [
                    {
                        "OAuth2PasswordBearer": [
                            "student"
                        ]
                    }
                ],
                "parameters": [
                    {
                        "name": "username",
                        "in": "query",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "title": "Username"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/StudentSchema"
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/v1/update/studentInfo": {
            "post": {
                "tags": [
                    "学生信息事务"
                ],
                "summary": "修改学生信息",
                "description": "通过token修改学生信息",
                "operationId": "修改学生信息_api_v1_update_studentInfo_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/StudentSchema"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/StdResp"
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                },
                "security": [
                    {
                        "OAuth2PasswordBearer": [
                            "student"
                        ]
                    }
                ]
            }
        },
        "/api/v1/post/studentInfo": {
            "post": {
                "tags": [
                    "学生信息事务"
                ],
                "summary": "创建学生信息",
                "description": "创建一个完整的学生信息",
                "operationId": "创建学生信息_api_v1_post_studentInfo_post",
                "requestBody": {
                    "required": true,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/StudentSchema"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/StdResp"
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            },
            "get": {
                "tags": [
                    "学生信息事务"
                ],
                "summary": "删除学生信息",
                "description": "删除一个学生的档案信息",
                "operationId": "删除学生信息_api_v1_post_studentInfo_get",
                "parameters": [
                    {
                        "name": "username",
                        "in": "query",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "title": "Username"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/StdResp"
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/v1/get/userManagerRole": {
            "post": {
                "tags": [
                    "学生信息事务"
                ],
                "summary": "获取学生的角色信息",
                "description": "通过token获取一个学生的信息",
                "operationId": "获取学生的角色信息_api_v1_get_userManagerRole_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/TokenSchema"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                },
                "security": [
                    {
                        "OAuth2PasswordBearer": [
                            "student"
                        ]
                    }
                ]
            }
        },
"""