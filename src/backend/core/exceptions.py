"""
异常处理模块
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