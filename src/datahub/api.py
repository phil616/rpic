from fastapi import APIRouter,Depends
from dependencies import GlobalDependency,get_state
from pydantic import BaseModel


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

@data_hub_router.get("/get/{mid}/{key}")
def get_object(mid:str,key:str,state:GlobalDependency=Depends(get_state)):
    o = state.get(mid)
    return o.get(key)

