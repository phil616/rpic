from fastapi import FastAPI
from control import app_lifespan
from api import data_hub_router as api_router
from datahub import curd_router
from authroize import authorize_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(lifespan=app_lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router,tags=['Admin'])
app.include_router(authorize_router,tags=['Authorize'])
app.include_router(curd_router,tags=['CURD'])