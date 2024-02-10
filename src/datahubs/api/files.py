from fastapi import APIRouter,UploadFile,File
from fastapi.responses import FileResponse

file_router = APIRouter(prefix="/file")

@file_router.get("/download")
async def download_file():
    ... 

@file_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    ...

@file_router.get("/filelist")
async def file_list():
    ...

@file_router.get("/fileinfo")
async def file_info():
    ...