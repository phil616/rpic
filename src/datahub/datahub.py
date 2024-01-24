from fastapi import APIRouter,Depends
from dependencies import get_state,GlobalDependency
from pydantic import BaseModel
from control import SQLDB
from fastapi import Request
curd_router = APIRouter()

class DataSchema(BaseModel):
    key:str
    value:str

@curd_router.get("/cache/get/{cache_id}/{key}")
async def get_cache_by_key(cache_id:str,key:str,state:GlobalDependency=Depends(get_state)):
    return state.memories[cache_id].get(key)

@curd_router.post("/cache/set/{cache_id}")
async def set_cache_by_schema(data:DataSchema,cache_id:str,state:GlobalDependency=Depends(get_state)):
    state.memories[cache_id].set(data.key,data.value)

@curd_router.get("/cache/delete/{cache_id}/{key}")
async def delete_cache_by_key(cache_id:str,key:str,state:GlobalDependency=Depends(get_state)):
    return state.memories[cache_id].delete(key)

@curd_router.get("/disk/get/{disk_id}/{key}")
async def get_disk_by_key(disk_id:str,key:str,state:GlobalDependency=Depends(get_state)):
    return state.diskes[disk_id].get(key)

@curd_router.post("/disk/set/{disk_id}")
async def set_disk_by_schema(data:DataSchema,disk_id:str,state:GlobalDependency=Depends(get_state)):
    state.diskes[disk_id].set(data.key,data.value)
    return data.key

@curd_router.get("/disk/delete/{disk_id}/{key}")
async def delete_disk_by_key(disk_id:str,key:str,state:GlobalDependency=Depends(get_state)):
    return state.diskes[disk_id].delete(key)

@curd_router.get("/disk/submit/{disk_id}")
async def submit_disk_by_key(disk_id:str,state:GlobalDependency=Depends(get_state)):
    return state.diskes[disk_id].submit()


@curd_router.get("/db/get/userspace")
async def get_sqldb_username_space(req:Request):
    alljson = await SQLDB.filter(username=req.app.state.username).all()
    return alljson

@curd_router.post("/db/set/userspace")
async def set_sqldb_username_space(data:DataSchema,req:Request):
    raise NotImplementedError


@curd_router.get("/json/new")
async def new_json(req:Request):
    ...

@curd_router.get("/json/get/{id}/{key}")
async def get_json_by_key(id:str,key:str,req:Request):
    ...