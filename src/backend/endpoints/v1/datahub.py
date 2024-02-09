from fastapi import APIRouter

datahub_router = APIRouter(prefix="/datahub")

@datahub_router.get("/ids")
async def get_datahub_ids():
    pass

@datahub_router.get("/info")
async def get_datahub_info():
    pass
