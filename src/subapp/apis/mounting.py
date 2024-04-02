from fastapi import APIRouter,Depends,FastAPI
from core.dependencies import GlobalState,get_global_state
from core.exceptions import HTTP_E404,HTTP_E403
mounting_router = APIRouter("/mount")

def mount_router_to_app(app:FastAPI,function:callable):
    ...