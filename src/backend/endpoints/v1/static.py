from fastapi import APIRouter
from fastapi.responses import RedirectResponse

static_router = APIRouter()

@static_router.get("/")
async def get_index():
    return RedirectResponse(url="/static/index.html")