from fastapi import APIRouter

root_router = APIRouter("/root")


@root_router.post("/post")
async def mount_root_function():
    ...