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
from dataobj import g_cache,g_disk
from webcore.dependencies import GlobalState, get_global_state
from webcore.authorize import check_permissions
from pydantic import BaseModel


http_interface_router = APIRouter(prefix="/http",dependencies=[Security(check_permissions,scopes=["PROCEDURE:ADMIN"])])


class KVPair(BaseModel):
    key:str
    value:str

# for http data object interface, api router should provide following endpoints


async def http_interface_cache_create(data:KVPair, state:GlobalState=Depends(get_global_state)):
    g_cache.get_cache(state.user.get("gid")).set(data.key,data.value)
    return {"status":"ok"}
async def http_interface_cache_update(data:KVPair, state:GlobalState=Depends(get_global_state)):
    g_cache.get_cache(state.user.get("gid")).update(data.key,data.value)
    return {"status":"ok"}

async def http_interface_cache_get(key:str, state:GlobalState=Depends(get_global_state)):
    return {"value":g_cache.get_cache(state.user.get("gid")).get(key)}
async def http_interface_cache_delete(key:str, state:GlobalState=Depends(get_global_state)):
    g_cache.get_cache(state.user.get("gid")).delete(key)
    return {"status":"ok"}

async def http_interface_disk_create(data:KVPair, state:GlobalState=Depends(get_global_state)):
    g_disk.get_disk(state.user.get("gid")).set(data.key,data.value)
    return {"status":"ok"}

async def http_interface_disk_update(data:KVPair, state:GlobalState=Depends(get_global_state)):
    g_disk.get_disk(state.user.get("gid")).update(data.key,data.value)
    return {"status":"ok"}


async def http_interface_disk_get(key:str, state:GlobalState=Depends(get_global_state)):
    return {"value":g_disk.get_disk(state.user.get("gid")).get(key)}

async def http_interface_disk_delete(key:str, state:GlobalState=Depends(get_global_state)):
    g_disk.get_disk(state.user.get("gid")).delete(key)
    return {"status":"ok"}

http_interface_router.post("/cache/create")(http_interface_cache_create)
http_interface_router.post("/cache/update")(http_interface_cache_update)
http_interface_router.post("/cache/get")(http_interface_cache_get)
http_interface_router.post("/cache/delete")(http_interface_cache_delete)

http_interface_router.post("/disk/create")(http_interface_disk_create)
http_interface_router.post("/disk/update")(http_interface_disk_update)
http_interface_router.post("/disk/get")(http_interface_disk_get)
http_interface_router.post("/disk/delete")(http_interface_disk_delete)