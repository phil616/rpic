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

from fastapi import APIRouter,FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi import Request
from conf import config

openapi_router = APIRouter()

def custom_openapi(app:FastAPI):
    print("debug, custom_openapi called")
    # operate openapi_schema's routes here
    for r in app.routes:
        print(r)
    
    openapi_schema = get_openapi(
        title=config.APP_TITLE,
        version=config.APP_VERSION,
        description=config.APP_DESCRIPTION,
        routes=app.routes,  
    )

    # operate the openapi_schema here
    print(openapi_schema)
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@openapi_router.get("/openapi.json", include_in_schema=False)
async def get_openapi_json(req:Request):
    openapi_schema = get_openapi(
        title=config.APP_TITLE,
        version=config.APP_VERSION,
        description=config.APP_DESCRIPTION,
        routes=req.app.routes,  
    )
    return openapi_schema


