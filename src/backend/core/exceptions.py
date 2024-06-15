"""
异常处理模块
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
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Optional, Any
from core.logcontroller import log as logger

def HTTP_E401(details: Optional[Any] = None, headers: Optional[dict[str, Any]] = None) -> None:
    logger.exception(f"HTTP_E401: {details}")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=details,
        headers=headers
    )

def HTTP_E403(details: Optional[Any] = None, headers: Optional[dict[str, Any]] = None) -> None:
    logger.exception(f"HTTP_E403: {details}")
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=details,
        headers=headers
    )

def HTTP_E404(details: Optional[Any] = None, headers: Optional[dict[str, Any]] = None) -> None:
    logger.exception(f"HTTP_E404: {details}")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=details,
        headers=headers
    )
async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """
    http异常处理
    :param _:
    :param exc:
    :return:
    """
    if exc.status_code == 401:
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

    return JSONResponse({
        "code": exc.status_code,
        "message": exc.detail,
        "data": exc.detail
    }, status_code=exc.status_code, headers=exc.headers)

async def orm_error_handler(_: Request, exc: Exception) -> JSONResponse:
    """
    orm异常处理
    :param _:
    :param exc:
    :return:
    """
    logger.exception(f"ORM Exception: {exc}")
    return JSONResponse({
        "code": 500,
        "message": "ORM Exception",
        "data": str(exc)
    }, status_code=500)