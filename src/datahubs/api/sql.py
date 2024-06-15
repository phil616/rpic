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

from fastapi import APIRouter,Depends,Security
from dataobj import sqlobj
from webcore.dependencies import GlobalState, get_global_state
from webcore.authorize import check_permissions


http_interface_router = APIRouter(prefix="/sql",dependencies=[Security(check_permissions,scopes=["PROCEDURE:ADMIN"])])

async def http_interface_disk_delete(sql:str, state:GlobalState=Depends(get_global_state)):
    result = sqlobj.execute_sql(sql, state.user.get("gid"))
    return result

http_interface_router.post("/execute")(http_interface_disk_delete)