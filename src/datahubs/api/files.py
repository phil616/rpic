"""
开发者原创性与版权声明
该注释用于声明作者（开发者）具有该文件或代码的所有权利
作者承诺该源码具有原创性和唯一性
除法律约束的其他行为和上游协议外，该代码作者具有所有权利
作者承诺代码的原创性和完整性
作者：费东旭
最后一次更改日期：2024年6月10日（北京时间）
通讯地址：吉林省长春市朝阳区卫星路6543号长春大学计算机科学技术学院
通讯方式：phil616@163.com

"""

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