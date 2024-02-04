from .v1.openapi import openapi_router
from .v1.static import static_router
from .v1.debug import debug_router
from .v1.user import user_router
from .v1.token import token_router


from fastapi import APIRouter
all_router = APIRouter()

all_router.include_router(openapi_router)
all_router.include_router(static_router)
all_router.include_router(debug_router)
all_router.include_router(token_router)
all_router.include_router(user_router)
