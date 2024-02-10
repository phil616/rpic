from .v1.openapi import openapi_router
from .v1.static import static_router
from .v1.debug import debug_router
from .v1.user import user_router
from .v1.token import token_router
from .v1.datahub import datahub_router
from .v1.group import group_router
from fastapi import APIRouter
all_router = APIRouter()

all_router.include_router(openapi_router,tags=["openapi"])
all_router.include_router(static_router,tags=["static"])
all_router.include_router(debug_router,tags=["debug"])
all_router.include_router(token_router,tags=["token"])

all_router.include_router(user_router,tags=["user"])
all_router.include_router(datahub_router,tags=["datahub"])
all_router.include_router(group_router,tags=["group"])