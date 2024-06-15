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


from endpoints.v1.openapi import openapi_router
from endpoints.v1.static import static_router
from endpoints.v1.debug import debug_router
from endpoints.v1.user import user_router
from endpoints.v1.token import token_router
from endpoints.v1.datahub import datahub_router
from endpoints.v1.group import group_router
from endpoints.v1.machines import machine_router
from endpoints.v1.runtime import runtime_router
from endpoints.v1.mounting import mounting_router
from endpoints.v1.procedure import procedure_router
from fastapi import APIRouter
all_router = APIRouter()

all_router.include_router(openapi_router,tags=["openapi"])
all_router.include_router(static_router,tags=["static"])
all_router.include_router(debug_router,tags=["debug"])
all_router.include_router(token_router,tags=["token"])

all_router.include_router(user_router,tags=["user"])
all_router.include_router(datahub_router,tags=["datahub"])

all_router.include_router(group_router,tags=["group"])
all_router.include_router(machine_router,tags=["machine"])


all_router.include_router(runtime_router,tags=['runtime'])
all_router.include_router(mounting_router,tags=['procedure'])
all_router.include_router(procedure_router,tags=['procedure'])