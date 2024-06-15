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

from fastapi import APIRouter, Security
from core.authorize import check_permissions
from core.proxy import request
from core.exceptions import HTTP_E401,HTTP_E404
from pydantic import BaseModel,Field
from typing import Optional,Literal,Union,Dict
from core.utils import generate_random_string,str_to_bytes,bytes_to_str
from models.Procedure import Procedure
from models.ProcedureInfo import ProcedureInfo
procedure_router = APIRouter(prefix="/procedure",dependencies=[Security(check_permissions,scopes=["PROCEDURE:ADMIN"])])

class ProcedurePostSchema(BaseModel):
    procedure_raw:str
    procedure_name:Optional[str] = Field(default=generate_random_string())
    procedure_type:Literal["script","package"] = Field(default="package")   #Cases for type: Execute Type:[MOUNT ONLY,EXECUTE ONLY,MOUNT AND EXECUTE]
    procedure_encrypt_type:Optional[Literal["AES","SM4"]] = Field(default="AES")
    procedure_decrypt_key:str
    procedure_extra:Optional[str]

###########################
#    PROCEURE CURD        # 
#    PROCEDURE INFO CURD  #  UNION
###########################

# P C
@procedure_router.post("/create")
async def procedure_create_raw(p:ProcedurePostSchema):
    uid = request.userinfo.get("uid")
    gid = request.userinfo.get("gid")
    if not gid:
        HTTP_E401("Group Required")
    model_p = await Procedure.create(procedure_creator=uid,
                           procedure_group_id=gid,
                           memory_id=gid,
                           disk_id=gid,
                           **p.model_dump()
                           )
    pid = model_p.procedure_id
    await  ProcedureInfo.create(
        procedure_id=pid,
        **p.model_dump()
    )
    return {"procedure_id":pid}
# P D
@procedure_router.get("/delete")
async def procedure_delete_id(pid:int):
    p = await Procedure.filter(procedure_id=pid).first()
    await p.delete()
# P U
@procedure_router.post("/update")
async def procedure_update_schema():
    ...
# P R
@procedure_router.get("/get")
async def procedure_get_id(pid:int):
    pmodel = {}
    p = Procedure.filter(procedure_id=pid).first()
    pi = ProcedureInfo.filter(procedure_id=pid).first()
    pmodel.update(p.__dict__)
    pmodel.update(pi.__dict__)
    return pmodel


@procedure_router.get("/list")
async def procedure_list():
    uid = request.userinfo.get("uid")
    gid = request.userinfo.get("gid")
    if not gid:
        HTTP_E401("Group Required")
    pmodel = []
    ps = await Procedure.filter(procedure_group_id=gid).all()
    for p in ps:
        pi = await ProcedureInfo.filter(procedure_id=p.procedure_id).first()
        pmodel.append({**p.__dict__,**pi.__dict__})
    return pmodel
