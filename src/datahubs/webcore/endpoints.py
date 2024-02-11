from fastapi import APIRouter
from api.files import file_router
from api.http import http_interface_router
all_router = APIRouter()


all_router.include_router(file_router)
all_router.include_router(http_interface_router)
