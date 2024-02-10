from fastapi import APIRouter
from api.files import file_router

router_center = APIRouter()


router_center.include_router(file_router)
