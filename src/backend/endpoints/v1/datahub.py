from fastapi import APIRouter
from fastapi import Security
from core.authorize import check_permissions
from conf import config
datahub_router = APIRouter(prefix="/datahub")

@datahub_router.get("/ids")
async def get_datahub_ids():
    pass

@datahub_router.get("/jwt"
                    #,dependencies=[Security(check_permissions, scopes=["datahub"])]
                    )
async def get_datahub_info():
    return {"key":config.JWT_SECRET_KEY, "algorithm":config.JWT_ALGORITHM}
