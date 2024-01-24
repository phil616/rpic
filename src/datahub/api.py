from fastapi import APIRouter,Depends,Request
from dependencies import GlobalDependency,get_state
from control import User
from pydantic import BaseModel
from typing import List
# MEMORY CURD
# DISK CURD

# DATA HUB CURD

data_hub_router = APIRouter()

@data_hub_router.post("/add/memory")
def add_memory_object(state:GlobalDependency=Depends(get_state)):
    mid = state.new_memory()
    return mid

@data_hub_router.post("/add/disk")
def add_disk_object(state:GlobalDependency=Depends(get_state)):
    did = state.new_disk()
    return did

@data_hub_router.get("/get/memory/{mid}")
def get_memory_object(mid:str,state:GlobalDependency=Depends(get_state)):
    m = state.get_memory(mid)
    return m

@data_hub_router.get("/get/disk/{did}")
def get_disk_object(did:str,state:GlobalDependency=Depends(get_state)):
    d = state.get_disk(did)
    return d

@data_hub_router.get("/delete/memory/{mid}")
def delete_memory_object(mid:str,state:GlobalDependency=Depends(get_state)):
    raise NotImplementedError

@data_hub_router.get("/delete/disk/{did}")
def delete_disk_object(did:str,state:GlobalDependency=Depends(get_state)):
    raise NotImplementedError

class ObjectResponseSchema(BaseModel):
    username:str
    diskes:List[str]
    memories:List[str]

@data_hub_router.get("/get/all/objects")
async def get_allobject(req:Request,state:GlobalDependency=Depends(get_state)):
    user = await User.filter(username=req.app.state.username).first()
    return ObjectResponseSchema(username=user.username,diskes=user.files,memories=user.memories)
