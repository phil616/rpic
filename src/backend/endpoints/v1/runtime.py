from fastapi import APIRouter
from fastapi import Depends
from core.runtime import get_global_state,GlobalState
runtime_router = APIRouter(prefix="/runtime")

@runtime_router.get("/get/services")
async def runtime_get_all_services(state:GlobalState = Depends(get_global_state)):
    return state.runtime.get("sp")
