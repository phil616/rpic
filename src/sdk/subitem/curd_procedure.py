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


# CURD Procedure

# Create -> get a pid
# Update
# Retrive
# Delete

# mount -> get a endpoint

import streamlit as st
from pydantic import BaseModel,Field
from typing import Optional,Literal
from net import HTTP
class ProcedurePostSchema(BaseModel):
    procedure_raw:str
    procedure_name:Optional[str]
    procedure_type:Literal["script","package"] = Field(default="package")   #Cases for type: Execute Type:[MOUNT ONLY,EXECUTE ONLY,MOUNT AND EXECUTE]
    procedure_encrypt_type:Optional[Literal["AES","SM4"]] = Field(default="AES")
    procedure_decrypt_key:str
    procedure_extra:Optional[str]
def create_procedure(body:ProcedurePostSchema):
    resp = HTTP.json_post("/procedure/create",body.model_dump())
    return resp.json()


def get_all_procedure():
    resp = HTTP.get("/procedure/list")
    return resp.json()

def inline_curd_procedure():
    st.title("过程管理")
    st.subheader("Create a procedure")
    st.markdown("""
## Only support python script
                """)
    key = st.text_input("解密密钥")

    raw = st.text_area("Procedure raw",value="import cv2\nprint(\"hello\")")

    if st.button("Create"):
        current_procedure = ProcedurePostSchema(
            procedure_raw=raw,
            procedure_name="test",
            procedure_type="script",
            procedure_encrypt_type="AES",
            procedure_decrypt_key=key,
            procedure_extra="test"
        )
        resp = create_procedure(current_procedure)
        st.toast(resp)
    st.markdown("""---""")

    st.subheader("Get all procedure")
    resp = get_all_procedure()
    st.write(resp)