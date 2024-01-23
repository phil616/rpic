from fastapi import FastAPI
from control import app_lifespan
from api import data_hub_router as api_router
from authroize import authorize_router
app = FastAPI(lifespan=app_lifespan)

app.include_router(api_router)
app.include_router(authorize_router)